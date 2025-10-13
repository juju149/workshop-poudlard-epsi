# 📋 Technical Documentation - Magic Box

## Architecture Overview

### Design Pattern
The Magic Box tool follows a modular object-oriented design with clear separation of concerns:

- **MagicBox Class**: Core functionality encapsulated in a reusable class
- **Main Function**: CLI interface and argument parsing
- **Cross-Platform**: Uses C++17 std::filesystem for platform independence

### Class Structure

```cpp
class MagicBox {
    // Core functionality
    void scanWorkshopFiles(const std::vector<std::string>& extensions);
    void createArchive(const std::string& outputPath);
    void displayStatistics() const;
    
private:
    fs::path rootPath_;                    // Root directory to scan
    std::vector<fs::path> collectedFiles_; // List of collected files
};
```

## Technical Specifications

### Language & Standards
- **Language**: C++17
- **Standard Library**: std::filesystem (C++17)
- **Build System**: CMake 3.15+
- **Compiler Requirements**:
  - GCC 8.0+ (Linux)
  - Clang 9.0+ (macOS)
  - MSVC 2019+ (Windows)

### Key Dependencies
- Standard C++ Library (no external dependencies)
- std::filesystem for file system operations
- std::map for statistics aggregation
- std::vector for file list management

### Platform-Specific Features

#### Linux
```cmake
target_link_libraries(magic-box stdc++fs)
```
- Links with stdc++fs for filesystem support on older GCC versions

#### Windows
```cmake
add_compile_definitions(_CRT_SECURE_NO_WARNINGS)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
```
- Disables CRT warnings for fopen/strcpy
- Enables symbol exports for DLL builds (future)

## File Operations

### Scanning Algorithm
```
1. Start from root directory
2. Recursively iterate through all subdirectories
3. For each file:
   a. Check if in excluded directory (.git, build)
   b. Check if extension matches filter (if specified)
   c. Add to collected files list
4. Return collected files
```

### Exclusion Rules
- `.git/` directories (all subdirectories)
- `build/` directories (all subdirectories)
- Platform-specific exclusions automatically handled

### Archive Creation
```
1. Create output directory structure
2. For each collected file:
   a. Calculate relative path from root
   b. Create parent directories in archive
   c. Copy file preserving structure
3. Report success/failure
```

## CMake Configuration

### Build Types
- **Debug**: `-O0 -g` (default for development)
- **Release**: `-O3 -DNDEBUG` (optimized for production)

### Output Directories
```cmake
CMAKE_RUNTIME_OUTPUT_DIRECTORY = ${CMAKE_BINARY_DIR}/bin
CMAKE_LIBRARY_OUTPUT_DIRECTORY = ${CMAKE_BINARY_DIR}/lib
CMAKE_ARCHIVE_OUTPUT_DIRECTORY = ${CMAKE_BINARY_DIR}/lib
```

### Compiler Flags

**MSVC (Windows)**:
```cmake
/W4  # Warning level 4
```

**GCC/Clang (Linux/macOS)**:
```cmake
-Wall -Wextra -Wpedantic  # All warnings
```

## Performance Characteristics

### Time Complexity
- Scanning: O(n) where n = number of files in directory tree
- Filtering: O(n) where n = number of files found
- Archive creation: O(n) where n = number of collected files
- Total: **O(n)** linear time

### Space Complexity
- File list storage: O(n) where n = number of collected files
- Statistics map: O(e) where e = number of unique extensions
- Total: **O(n)** linear space

### Scalability
- Handles thousands of files efficiently
- Memory usage proportional to number of files
- No hardcoded limits on file counts

## Error Handling

### Exception Handling Strategy
```cpp
try {
    // File system operations
} catch (const fs::filesystem_error& e) {
    // Handle filesystem-specific errors
} catch (const std::exception& e) {
    // Handle general exceptions
}
```

### Error Categories
1. **Invalid Path**: Root directory doesn't exist
2. **Permission Denied**: Cannot read file/directory
3. **I/O Error**: Disk full, network error, etc.
4. **Memory Error**: Out of memory for large file lists

### Recovery Strategies
- Skip unreadable files and continue
- Display warnings for individual failures
- Throw exceptions only for fatal errors

## Testing Strategy

### Unit Test Scenarios
1. **Empty Directory**: Should return 0 files
2. **Single File**: Should collect exactly 1 file
3. **Multiple Extensions**: Should filter correctly
4. **Nested Directories**: Should preserve structure
5. **Excluded Directories**: Should skip .git and build

### Integration Test Scenarios
1. **Full Workshop Scan**: Test with real workshop structure
2. **Large Directory Tree**: Performance test with 1000+ files
3. **Cross-Platform Paths**: Test on Linux and Windows
4. **Invalid Inputs**: Test error handling

### Manual Testing Checklist
- [ ] Compilation on Linux (GCC)
- [ ] Compilation on Windows (MSVC)
- [ ] Compilation on macOS (Clang)
- [ ] Help display works
- [ ] Stats-only mode works
- [ ] Archive creation works
- [ ] Extension filtering works
- [ ] Directory exclusion works
- [ ] Large directory handling
- [ ] Error messages are clear

## Build Configuration

### Debug Build
```bash
cmake -DCMAKE_BUILD_TYPE=Debug ..
cmake --build .
```
- Includes debug symbols
- No optimization
- Useful for development

### Release Build
```bash
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build .
```
- Full optimization (-O3)
- No debug symbols
- Smaller binary size
- Faster execution

### Static Linking (Optional)
For portable binaries without dependencies:
```cmake
set(CMAKE_EXE_LINKER_FLAGS "-static")
```

## Installation

### System-Wide Installation
```bash
cd build
sudo cmake --install .
```

Installs to:
- Binary: `/usr/local/bin/magic-box`
- Documentation: `/usr/local/share/doc/magic-box/`

### Custom Prefix
```bash
cmake -DCMAKE_INSTALL_PREFIX=/opt/magic-box ..
cmake --build .
cmake --install .
```

## Future Enhancements

### Planned Features
1. **Compression Support**
   - ZIP format support
   - TAR.GZ for Linux
   - 7z for better compression

2. **.gitignore Support**
   - Parse .gitignore files
   - Respect exclusion patterns
   - Custom ignore files

3. **Progress Bar**
   - Visual progress for large scans
   - ETA estimation
   - Cancel capability

4. **Parallel Processing**
   - Multi-threaded file scanning
   - Concurrent file copying
   - Performance boost for large dirs

5. **Configuration File**
   - YAML/JSON config support
   - Preset profiles
   - Default exclusions

6. **JSON/CSV Export**
   - Machine-readable statistics
   - Integration with other tools
   - Data analysis support

### Architecture Evolution
- Plugin system for custom filters
- Network/cloud storage support
- Incremental backup capability
- File deduplication
- Encryption support

## Security Considerations

### Current Security
- No external dependencies = smaller attack surface
- No network operations = no remote exploits
- Local file access only = no privilege escalation

### Best Practices
- Always validate user input paths
- Use std::filesystem for safe path operations
- Avoid buffer overflows with std::string
- Handle symbolic links carefully

### Known Limitations
- No file content validation
- Follows symbolic links (potential loop)
- No file size limits (memory constraint)
- No virus/malware scanning

## Troubleshooting Guide

### Common Issues

**Issue**: `cmake` command not found
- **Solution**: Install CMake from cmake.org or package manager

**Issue**: Compiler errors with std::filesystem
- **Solution**: Ensure C++17 support (GCC 8+, Clang 9+, MSVC 2019+)

**Issue**: Link errors with filesystem
- **Solution**: Add `-lstdc++fs` linker flag (automatic in CMakeLists.txt)

**Issue**: Permission denied when scanning
- **Solution**: Run with appropriate permissions or change target directory

**Issue**: Very slow on network drives
- **Solution**: Copy to local disk first or use -s for stats only

## Performance Optimization Tips

### For Large Directories
1. Use `-s` flag first to estimate
2. Filter by specific extensions
3. Exclude large binary directories
4. Use SSD for faster I/O

### For Better Compilation Times
```bash
# Use parallel build
cmake --build . -j$(nproc)

# Use ccache (Linux)
export CXX="ccache g++"
cmake ..
```

### For Smaller Binaries
```bash
# Strip symbols (Linux)
strip build/bin/magic-box

# Use release build
cmake -DCMAKE_BUILD_TYPE=Release ..
```

## API Reference

### MagicBox Constructor
```cpp
MagicBox(const std::string& rootPath)
```
- **Parameters**: `rootPath` - Directory to scan
- **Throws**: `std::runtime_error` if path doesn't exist

### scanWorkshopFiles
```cpp
void scanWorkshopFiles(const std::vector<std::string>& extensions)
```
- **Parameters**: `extensions` - List of file extensions to include (empty = all)
- **Side Effects**: Populates internal file list

### createArchive
```cpp
void createArchive(const std::string& outputPath)
```
- **Parameters**: `outputPath` - Destination directory
- **Throws**: `fs::filesystem_error` on I/O failure

### displayStatistics
```cpp
void displayStatistics() const
```
- **No Parameters**
- **Output**: Prints statistics to stdout

### getCollectedFiles
```cpp
const std::vector<fs::path>& getCollectedFiles() const
```
- **Returns**: Reference to collected files list

## License & Credits

Developed for **Workshop Poudlard à l'EPSI/WIS 2025**
Challenge #14 - La Boite Magique de Severus Rogue

**Deadline**: 16/10/2025
**Story Points**: 8
**Lead**: Frontend Copilot
**Documentation**: Documentation Copilot

---

*This technical documentation is maintained as part of the project deliverables.*
