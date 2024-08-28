# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Basic functionality for eBay, Depop, and Vinted integrations
- Image upload support for all platforms
- Cross-platform search functionality (eBay only for now)

### Changed
- Updated main.py to handle image paths in listing details
- Improved error handling across all platform-specific files

### Fixed
- Various bug fixes and code improvements

## [0.1.0] - 2024-[28/08]

### Added
- main.py:
  - Import for 'os' module
  - Updated 'get_listing_details' function to handle image paths
  - Modified 'create_listing' function to pass the entire listing dictionary

- depop.py:
  - 'upload_image' function
  - Updated 'create_listing' function to handle image uploads
  - Improved error handling

- vinted.py:
  - Import for 'os' module
  - 'upload_image' function
  - Updated 'create_listing' function to handle image uploads
  - Improved error handling

- ebay.py:
  - Import for 'os' module
  - 'upload_image' function
  - Updated 'create_listing' function to handle image uploads
  - Improved error handling in 'create_listing' and 'search_listings'
  - Modified 'search_listings' to accept 'config' parameter

### Changed
- Updated README.md with project overview, setup instructions, and MIT License
- Created initial documentation structure

### Known Issues
- Depop and Vinted integrations are not fully implemented and tested
- Category mapping is not yet implemented for any platform
- Error handling needs further improvement
- Configuration management needs to be implemented

[Unreleased]: https://github.com/yourusername/your-repo-name/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/your-repo-name/releases/tag/v0.1.0