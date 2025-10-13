#include <iostream>
#include <vector>
#include <string>
#include "MagicBox.h"

void printBanner() {
    std::cout << R"(
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🧪 LA BOITE MAGIQUE DE SEVERUS ROGUE 🧪                 ║
║                                                              ║
║    Cross-Platform Workshop Archive Tool                     ║
║    Poudlard à l'EPSI/WIS                                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
)" << std::endl;
}

void printUsage(const char* programName) {
    std::cout << "Usage: " << programName << " [options]" << std::endl;
    std::cout << "\nOptions:" << std::endl;
    std::cout << "  -h, --help              Show this help message" << std::endl;
    std::cout << "  -r, --root <path>       Root directory to scan (default: current directory)" << std::endl;
    std::cout << "  -o, --output <path>     Output archive directory (default: ./workshop-archive)" << std::endl;
    std::cout << "  -e, --ext <extensions>  File extensions to include (comma-separated, e.g., .cpp,.h,.md)" << std::endl;
    std::cout << "  -s, --stats             Display statistics only (no archive creation)" << std::endl;
    std::cout << "\nExamples:" << std::endl;
    std::cout << "  " << programName << " -r . -o ./archive" << std::endl;
    std::cout << "  " << programName << " -r ~/workshop -e .cpp,.h,.md,.py" << std::endl;
    std::cout << "  " << programName << " -s -e .cpp,.h" << std::endl;
}

std::vector<std::string> parseExtensions(const std::string& extString) {
    std::vector<std::string> extensions;
    std::string current;
    
    for (char c : extString) {
        if (c == ',') {
            if (!current.empty()) {
                extensions.push_back(current);
                current.clear();
            }
        } else if (!std::isspace(c)) {
            current += c;
        }
    }
    
    if (!current.empty()) {
        extensions.push_back(current);
    }
    
    return extensions;
}

int main(int argc, char* argv[]) {
    printBanner();
    
    std::string rootPath = ".";
    std::string outputPath = "./workshop-archive";
    std::vector<std::string> extensions;
    bool statsOnly = false;
    
    // Parse command line arguments
    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        
        if (arg == "-h" || arg == "--help") {
            printUsage(argv[0]);
            return 0;
        } else if (arg == "-r" || arg == "--root") {
            if (i + 1 < argc) {
                rootPath = argv[++i];
            } else {
                std::cerr << "Error: --root requires a path argument" << std::endl;
                return 1;
            }
        } else if (arg == "-o" || arg == "--output") {
            if (i + 1 < argc) {
                outputPath = argv[++i];
            } else {
                std::cerr << "Error: --output requires a path argument" << std::endl;
                return 1;
            }
        } else if (arg == "-e" || arg == "--ext") {
            if (i + 1 < argc) {
                extensions = parseExtensions(argv[++i]);
            } else {
                std::cerr << "Error: --ext requires extension list" << std::endl;
                return 1;
            }
        } else if (arg == "-s" || arg == "--stats") {
            statsOnly = true;
        } else {
            std::cerr << "Unknown option: " << arg << std::endl;
            printUsage(argv[0]);
            return 1;
        }
    }
    
    try {
        MagicBox magicBox(rootPath);
        
        std::cout << "🎯 Configuration:" << std::endl;
        std::cout << "  Root path: " << rootPath << std::endl;
        std::cout << "  Output path: " << outputPath << std::endl;
        if (!extensions.empty()) {
            std::cout << "  Extensions: ";
            for (size_t i = 0; i < extensions.size(); i++) {
                std::cout << extensions[i];
                if (i < extensions.size() - 1) std::cout << ", ";
            }
            std::cout << std::endl;
        } else {
            std::cout << "  Extensions: all files" << std::endl;
        }
        std::cout << std::endl;
        
        // Scan files
        magicBox.scanWorkshopFiles(extensions);
        
        // Display statistics
        magicBox.displayStatistics();
        
        // Create archive unless stats-only mode
        if (!statsOnly) {
            std::cout << std::endl;
            magicBox.createArchive(outputPath);
        }
        
        std::cout << "\n✨ Magic complete! ✨" << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "\n❌ Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
