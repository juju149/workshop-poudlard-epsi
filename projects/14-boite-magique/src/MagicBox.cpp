#include "MagicBox.h"
#include <iostream>
#include <fstream>
#include <algorithm>
#include <map>

MagicBox::MagicBox(const std::string& rootPath) : rootPath_(rootPath) {
    if (!fs::exists(rootPath_)) {
        throw std::runtime_error("Root path does not exist: " + rootPath);
    }
}

void MagicBox::scanWorkshopFiles(const std::vector<std::string>& extensions) {
    collectedFiles_.clear();
    
    std::cout << "🔍 Scanning workshop files..." << std::endl;
    
    try {
        for (const auto& entry : fs::recursive_directory_iterator(rootPath_)) {
            if (entry.is_regular_file()) {
                // Skip .git directories
                std::string pathStr = entry.path().string();
                if (pathStr.find("/.git/") != std::string::npos || 
                    pathStr.find("\\.git\\") != std::string::npos) {
                    continue;
                }
                
                // Skip build directories
                if (pathStr.find("/build/") != std::string::npos || 
                    pathStr.find("\\build\\") != std::string::npos) {
                    continue;
                }
                
                if (extensions.empty() || isValidExtension(entry.path(), extensions)) {
                    collectedFiles_.push_back(entry.path());
                }
            }
        }
    } catch (const fs::filesystem_error& e) {
        std::cerr << "⚠️  Error scanning directory: " << e.what() << std::endl;
    }
    
    std::cout << "✅ Found " << collectedFiles_.size() << " files" << std::endl;
}

bool MagicBox::isValidExtension(const fs::path& file, 
                                 const std::vector<std::string>& extensions) const {
    std::string ext = file.extension().string();
    return std::find(extensions.begin(), extensions.end(), ext) != extensions.end();
}

void MagicBox::createArchive(const std::string& outputPath) {
    fs::path archivePath(outputPath);
    
    std::cout << "📦 Creating archive at: " << archivePath << std::endl;
    
    try {
        // Create output directory if it doesn't exist
        if (archivePath.has_parent_path()) {
            fs::create_directories(archivePath.parent_path());
        }
        
        // Create the archive directory
        if (fs::exists(archivePath)) {
            fs::remove_all(archivePath);
        }
        fs::create_directories(archivePath);
        
        // Copy files while preserving directory structure
        for (const auto& file : collectedFiles_) {
            fs::path relativePath = fs::relative(file, rootPath_);
            fs::path destPath = archivePath / relativePath;
            
            // Create parent directories
            if (destPath.has_parent_path()) {
                fs::create_directories(destPath.parent_path());
            }
            
            // Copy file
            copyToArchive(file, destPath);
        }
        
        std::cout << "✅ Archive created successfully!" << std::endl;
        std::cout << "📂 Location: " << fs::absolute(archivePath) << std::endl;
        
    } catch (const fs::filesystem_error& e) {
        std::cerr << "❌ Error creating archive: " << e.what() << std::endl;
        throw;
    }
}

void MagicBox::copyToArchive(const fs::path& source, const fs::path& destination) {
    try {
        fs::copy(source, destination, 
                 fs::copy_options::overwrite_existing);
    } catch (const fs::filesystem_error& e) {
        std::cerr << "⚠️  Could not copy " << source << ": " << e.what() << std::endl;
    }
}

void MagicBox::displayStatistics() const {
    std::cout << "\n📊 Workshop Statistics" << std::endl;
    std::cout << "=====================" << std::endl;
    std::cout << "Total files collected: " << collectedFiles_.size() << std::endl;
    
    // Count by extension
    std::map<std::string, int> extensionCount;
    for (const auto& file : collectedFiles_) {
        std::string ext = file.extension().string();
        if (ext.empty()) ext = "[no extension]";
        extensionCount[ext]++;
    }
    
    std::cout << "\nFiles by type:" << std::endl;
    for (const auto& [ext, count] : extensionCount) {
        std::cout << "  " << ext << ": " << count << std::endl;
    }
}

const std::vector<fs::path>& MagicBox::getCollectedFiles() const {
    return collectedFiles_;
}

std::string MagicBox::executeCommand(const std::string& command) {
    std::string result;
    FILE* pipe = popen(command.c_str(), "r");
    if (pipe) {
        char buffer[128];
        while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
            result += buffer;
        }
        pclose(pipe);
    }
    // Remove trailing newline
    if (!result.empty() && result.back() == '\n') {
        result.pop_back();
    }
    return result;
}

std::string MagicBox::getGitConfig(const std::string& key) {
    return executeCommand("git config --global " + key + " 2>/dev/null");
}

void MagicBox::pushToGitHub(const std::string& archivePath, const std::string& githubUrl, const std::string& githubFolder, const std::string& githubBranch) {
    fs::path archiveDir(archivePath);
    std::cout << "\n🚀 Pushing to GitHub..." << std::endl;
    std::cout << "📂 Archive: " << fs::absolute(archiveDir) << std::endl;
    std::cout << "🔗 Repository: " << githubUrl << std::endl;
    if (!githubFolder.empty()) {
        std::cout << "📁 Target folder in repo: " << githubFolder << std::endl;
    }

    // Get git credentials
    std::string gitName = getGitConfig("user.name");
    std::string gitEmail = getGitConfig("user.email");

    if (gitName.empty() || gitEmail.empty()) {
        throw std::runtime_error("Git credentials not found. Please configure:\n"
                               "  git config --global user.name \"Your Name\"\n"
                               "  git config --global user.email \"your.email@example.com\"");
    }

    std::cout << "👤 Using Git credentials: " << gitName << " <" << gitEmail << ">" << std::endl;

    try {
        // Change to archive directory
        std::string originalPath = fs::current_path();
        fs::current_path(archiveDir);

        std::cout << "📝 Initializing git repository..." << std::endl;

        // Initialize git repo
        if (executeCommand("git init 2>&1").find("Initialized") == std::string::npos &&
            executeCommand("git status 2>&1").find("fatal") != std::string::npos) {
            executeCommand("git init");
        }

        // Configure git for this repo
        executeCommand("git config user.name \"" + gitName + "\"");
        executeCommand("git config user.email \"" + gitEmail + "\"");

        // Si dossier cible, déplacer le contenu dans ce dossier
        if (!githubFolder.empty()) {
            fs::path targetDir = archiveDir / githubFolder;
            fs::create_directories(targetDir);
            std::string rootSegment = fs::path(githubFolder).begin()->string();
            for (const auto& entry : fs::directory_iterator(archiveDir)) {
                // Ignore the target folder and any folder/file whose name matches the root segment
                if (entry.path() == targetDir || entry.path().filename() == rootSegment) continue;
                fs::path dest = targetDir / entry.path().filename();
                if (fs::is_directory(entry.path())) {
                    // Copie récursive du dossier
                    std::error_code ec;
                    fs::copy(entry.path(), dest, fs::copy_options::recursive | fs::copy_options::overwrite_existing, ec);
                    if (ec) std::cerr << "⚠️  Could not copy directory " << entry.path() << ": " << ec.message() << std::endl;
                } else {
                    // Déplacement du fichier
                    std::error_code ec;
                    fs::rename(entry.path(), dest, ec);
                    if (ec) std::cerr << "⚠️  Could not move file " << entry.path() << ": " << ec.message() << std::endl;
                }
            }
        }

        // Add all files
        std::cout << "📦 Adding files to git..." << std::endl;
        executeCommand("git add .");

        // Gestion de la branche cible (APRÈS avoir ajouté les fichiers)
        if (!githubBranch.empty()) {
            std::cout << "🌿 Target branch: " << githubBranch << std::endl;
            // Crée et switch sur la branche (si elle n'existe pas)
            std::string branchCheck = executeCommand("git branch --list " + githubBranch);
            if (branchCheck.empty()) {
                executeCommand("git checkout -b " + githubBranch);
            } else {
                executeCommand("git checkout " + githubBranch);
            }
        }

        // Create commit
        std::cout << "💾 Creating commit..." << std::endl;
        std::string commitMsg = "✨ Magic Box Archive - " + executeCommand("date '+%Y-%m-%d %H:%M:%S'");
        
        // Debug: vérifier l'état avant commit
        std::string statusCheck = executeCommand("git status --porcelain 2>&1");
        std::cout << "🔍 Debug - Git status: " << (statusCheck.empty() ? "no changes" : statusCheck) << std::endl;
        
        std::string commitResult = executeCommand("git commit -m \"" + commitMsg + "\" 2>&1");
        std::cout << "🔍 Debug - Commit result: " << commitResult << std::endl;
        
        // Si aucun changement à commiter, forcer un commit vide pour que la branche existe
        if (commitResult.find("nothing to commit") != std::string::npos || 
            commitResult.find("no changes added") != std::string::npos) {
            std::cout << "🔍 Debug - Forcing empty commit..." << std::endl;
            std::string emptyCommitResult = executeCommand("git commit --allow-empty -m \"" + commitMsg + " (empty)\" 2>&1");
            std::cout << "🔍 Debug - Empty commit result: " << emptyCommitResult << std::endl;
        }
        
        // Debug: vérifier qu'on a bien un commit
        std::string logCheck = executeCommand("git log --oneline -1 2>&1");
        std::cout << "🔍 Debug - Last commit: " << logCheck << std::endl;

        // Add remote if not exists
        std::string remoteCheck = executeCommand("git remote -v 2>/dev/null");
        if (remoteCheck.find("origin") == std::string::npos) {
            std::cout << "🔗 Adding GitHub remote..." << std::endl;
            executeCommand("git remote add origin " + githubUrl);
        }

        // Push to GitHub
        std::cout << "🚀 Pushing to GitHub..." << std::endl;
        std::string pushCmd;
        if (!githubBranch.empty()) {
            pushCmd = "git push -u origin " + githubBranch + " 2>&1";
        } else {
            pushCmd = "git push -u origin main 2>&1 || git push -u origin master 2>&1";
        }
        std::string pushResult = executeCommand(pushCmd);
        if (pushResult.find("error") != std::string::npos || 
            pushResult.find("fatal") != std::string::npos) {
            std::cerr << "⚠️  Push output: " << pushResult << std::endl;
        }

        // Restore original path
        fs::current_path(originalPath);

        std::cout << "✅ Successfully pushed to GitHub!" << std::endl;
        std::cout << "🌐 View your archive at: " << githubUrl << std::endl;

    } catch (const std::exception& e) {
        // Restore original path in case of error
        try { fs::current_path(fs::current_path().parent_path()); } catch (...) {}
        throw std::runtime_error("Failed to push to GitHub: " + std::string(e.what()));
    }
}
