from bs4 import BeautifulSoup

# Load your HTML file
with open("input.html", "r") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# List of allowed tags that you want to keep
allowed_tags = ["p", "a", "div", "blockquote", "sup", "sub", "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5", "h6", "strong", "em"]

# Remove all <style> and <link> tags
for style in soup.find_all(["style", "link"]):
    style.decompose()

# Remove all <span> tags but keep their content
for span in soup.find_all("span"):
    span.unwrap()  # removes the tag but keeps its content

# Remove all <svg> tags and their contents
for svg in soup.find_all("svg"):
    svg.decompose()  # removes the tag and its contents

# Strip all attributes from tags, except for href on <a> tags
for tag in soup.find_all(True):  # True finds all tags
    # If the tag is not in the allowed list, remove it entirely
    if tag.name not in allowed_tags:
        tag.decompose()
    else:
        # Remove all attributes except for 'href' in <a> tags
        tag.attrs = {k: v for k, v in tag.attrs.items() if tag.name == "a" and k == "href"}

# Save the cleaned HTML content
with open("output.html", "w") as file:
    file.write(soup.prettify())

