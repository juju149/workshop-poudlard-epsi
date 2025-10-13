#ifndef MAGIC_BOX_H
#define MAGIC_BOX_H

#include <string>
#include <vector>
#include <filesystem>

namespace fs = std::filesystem;

/**
 * @brief La Boite Magique de Severus Rogue
 * Cross-platform tool to collect and archive workshop sources and documents
 */
class MagicBox {
public:
    MagicBox(const std::string& rootPath);
    
    /**
     * @brief Scan directory for workshop files
     * @param extensions File extensions to include (e.g., {".cpp", ".md", ".py"})
     */
    void scanWorkshopFiles(const std::vector<std::string>& extensions);
    
    /**
     * @brief Create an archive of collected files
     * @param outputPath Path for the output archive
     */
    void createArchive(const std::string& outputPath);
    
    /**
     * @brief Display collected files statistics
     */
    void displayStatistics() const;
    
    /**
     * @brief Get list of collected files
     */
    const std::vector<fs::path>& getCollectedFiles() const;

private:
    fs::path rootPath_;
    std::vector<fs::path> collectedFiles_;
    
    bool isValidExtension(const fs::path& file, const std::vector<std::string>& extensions) const;
    void copyToArchive(const fs::path& source, const fs::path& destination);
};

#endif // MAGIC_BOX_H
