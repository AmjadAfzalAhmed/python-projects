import requests  # Helps fetch web pages
from bs4 import BeautifulSoup  # Helps read and understand web pages
import re  # Helps find patterns in text

"""
A web scraper program that extracts and displays the profile picture URL of a given GitHub user.  

It performs web scraping by:

1. Extracting the GitHub username from a provided profile or repository URL.
2. Sending an HTTP request to the GitHub profile page.
3. Parsing the HTML content to locate the profile image.
4. Displaying the direct URL of the profile image.
"""
# Function to extract username from GitHub URL
def get_github_username(url: str):
    
    # Use regex to extract username from URL
    match = re.search(r"github\.com/([^/]+)", url)
    return match.group(1) if match else None # Return username if found, else None

# Function to fetch profile image URL
def fetch_profile_image(username: str):
    # Construct URL from username
    profile_url = f"https://github.com/{username}"

    # Headers to prevent request blocking by GitHub. This line defines HTTP request headers, specifically setting the User-Agent header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    # Send HTTP GET request to GitHub profile
    response = requests.get(profile_url, headers=headers)

    # Check if request was successful
    if response.status_code != 200:
        return None  # Failed to fetch profile

    # Parse the HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the profile image (GitHub uses `alt="@username"` for the profile picture)
    profile_img_tag = soup.find("img", {"alt": f"@{username}"})

    # Return the profile image URL if found, else None
    return profile_img_tag["src"] if profile_img_tag and "src" in profile_img_tag.attrs else None

def main():
    # Main function to interact with the user
    print("\n✨ GitHub Profile Image Extractor ✨")
    print("----------------------------------")

    # Get input from user
    github_url = input("🔹 Enter GitHub profile or repository URL: ").strip()

    # Extract username
    username = get_github_username(github_url)
    if not username:
        print("❌ Invalid GitHub URL! Please enter a valid profile URL.")
        return

    # Fetch profile image
    profile_image = fetch_profile_image(username)

    # Display result
    if profile_image:
        print(f"\n✅ Profile Image URL: {profile_image}")
    else:
        print("\n❌ Profile image not found or GitHub blocked the request!")

if __name__ == "__main__": 
    main()
