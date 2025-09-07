#!/usr/bin/env python3
"""
Ubuntu-Inspired Image Fetcher
Wisdom of Ubuntu: "I am because we are"

This program connects to the global community of the internet, 
respectfully fetches shared resources, and organizes them for later appreciation.
"""

import os
import requests
import hashlib
from urllib.parse import urlparse, unquote
from pathlib import Path

def create_directory(directory_name="Fetched_Images"):
    """Create directory if it doesn't exist with Ubuntu spirit of community sharing"""
    try:
        os.makedirs(directory_name, exist_ok=True)
        print(f"✓ '{directory_name}' directory is ready for community sharing")
        return directory_name
    except OSError as e:
        print(f"✗ Respectful error creating directory: {e}")
        return None

def extract_filename(url, content_type=None):
    """Extract filename from URL or generate one based on content"""
    # Decode URL-encoded filename
    parsed = urlparse(url)
    path = unquote(parsed.path)
    
    # Try to get filename from URL path
    filename = os.path.basename(path)
    
    # If no filename or too generic, create one
    if not filename or '.' not in filename or len(filename) < 3:
        # Generate filename based on URL hash and content type
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        extension = get_extension_from_content_type(content_type) or '.jpg'
        filename = f"ubuntu_image_{url_hash}{extension}"
    elif '%' in filename:
        # Clean up any remaining URL encoding issues
        filename = unquote(filename)
    
    return filename

def get_extension_from_content_type(content_type):
    """Map content type to appropriate file extension"""
    if not content_type:
        return None
        
    content_map = {
        'image/jpeg': '.jpg',
        'image/jpg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/webp': '.webp',
        'image/svg+xml': '.svg',
        'image/bmp': '.bmp',
        'image/tiff': '.tiff'
    }
    
    return content_map.get(content_type.lower())

def is_duplicate_image(directory, content):
    """Check if image already exists to avoid duplicates (Ubuntu efficiency)"""
    # Create hash of image content
    content_hash = hashlib.md5(content).hexdigest()
    
    # Check all files in directory for matching hash
    for existing_file in os.listdir(directory):
        existing_path = os.path.join(directory, existing_file)
        if os.path.isfile(existing_path):
            try:
                with open(existing_path, 'rb') as f:
                    existing_hash = hashlib.md5(f.read()).hexdigest()
                    if existing_hash == content_hash:
                        return True, existing_file
            except IOError:
                continue
                
    return False, None

def download_image(url, directory="Fetched_Images"):
    """Respectfully fetch image from URL with Ubuntu principles"""
    if not url.startswith(('http://', 'https://')):
        print("✗ Please provide a valid URL starting with http:// or https://")
        return False
    
    print(f"🌐 Connecting to community resource: {url}")
    
    try:
        # Set respectful headers to identify ourselves
        headers = {
            'User-Agent': 'UbuntuImageFetcher/1.0 (Community Project)'
        }
        
        # Make request with timeout to respect community resources
        response = requests.get(url, headers=headers, timeout=10)
        
        # Check for HTTP errors respectfully
        response.raise_for_status()
        
        # Check content type to ensure we're downloading an image
        content_type = response.headers.get('Content-Type', '').split(';')[0]
        if not content_type.startswith('image/'):
            print(f"✗ Respectful notice: URL does not point to an image (Content-Type: {content_type})")
            return False
        
        # Check important HTTP headers for security
        security_headers = [
            'X-Content-Type-Options',
            'Content-Security-Policy',
            'X-Frame-Options'
        ]
        
        print("🔒 Security headers present:")
        for header in security_headers:
            value = response.headers.get(header)
            if value:
                print(f"   ✓ {header}: {value}")
        
        # Extract or generate filename
        filename = extract_filename(url, content_type)
        filepath = os.path.join(directory, filename)
        
        # Check for duplicate images
        is_duplicate, existing_file = is_duplicate_image(directory, response.content)
        if is_duplicate:
            print(f"✓ Image already exists in our community collection as '{existing_file}'")
            return True
        
        # Save the image with Ubuntu spirit of sharing
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        # Get file size for respectful reporting
        file_size = os.path.getsize(filepath)
        print(f"✓ Successfully fetched '{filename}' ({file_size} bytes)")
        print(f"✓ Image saved to {directory}/ for community appreciation")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Respectful connection error: {e}")
        return False
    except IOError as e:
        print(f"✗ Respectful file error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected but respectfully handled error: {e}")
        return False

def main():
    """Main function embodying Ubuntu principles"""
    print("\n" + "="*60)
    print("      Ubuntu-Inspired Image Fetcher")
    print("      'I am because we are'")
    print("="*60)
    
    # Create directory for community sharing
    directory = create_directory()
    if not directory:
        return
    
    # Prompt user for URL(s)
    urls_input = input("\n🌍 Enter image URL(s), separated by commas if multiple: ").strip()
    
    if not urls_input:
        print("✗ No URLs provided. We exist through sharing.")
        return
    
    # Handle multiple URLs
    urls = [url.strip() for url in urls_input.split(',') if url.strip()]
    successful_downloads = 0
    
    print(f"\n🔄 Processing {len(urls)} community resource(s)...")
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Fetching from: {url}")
        if download_image(url, directory):
            successful_downloads += 1
    
    # Ubuntu philosophy: report on community success
    print("\n" + "="*60)
    print(f"Community Sharing Complete!")
    print(f"Successfully fetched {successful_downloads} of {len(urls)} images")
    print("Thank you for participating in our global community")
    print("="*60)

if __name__ == "__main__":
    main()