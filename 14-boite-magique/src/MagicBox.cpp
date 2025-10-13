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
