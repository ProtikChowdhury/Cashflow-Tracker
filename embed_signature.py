import base64
import os

html_path = '/Users/protik/Documents/AntiGravity/1/expense_tracker.html'
image_path = '/Users/protik/.gemini/antigravity/brain/63f981ee-3f0a-42b7-9861-bad07418a170/uploaded_image_1768469650811.jpg'

def embed_signature():
    try:
        # Read image
        with open(image_path, 'rb') as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
        
        # Read HTML
        with open(html_path, 'r') as f:
            content = f.read()
        
        # Find the truncated tag we added earlier
        # We look for the start of the tag
        start_marker = '<img src="data:image/jpeg;base64,'
        end_marker = '" class="w-32'
        
        # Doing a robust replacement for the specific image tag we added
        # We know it ends with the class definition we added
        
        # Let's find the location
        start_idx = content.find(start_marker)
        if start_idx == -1:
            print("Error: Could not find the image tag start.")
            return

        # Find the closing quote of the src attribute from that position
        # The src attribute is followed by " class=...
        # So we look for the next "
        
        # Actually, simpler: replace the known truncated src with the full one.
        # But we don't know exactly where it was truncated in the file plain text without reading it.
        # So let's replace the whole IMG tag logic.
        
        # We'll search for the div wrapper content to ensure we target the right img
        target_section_start = '<!-- Signature -->'
        if target_section_start not in content:
            print("Error: Signature section not found")
            return
            
        # We will reconstruct the whole div to be safe
        new_div = f'''    <!-- Signature -->
    <div class="fixed bottom-6 right-6 z-50 flex flex-col items-center pointer-events-none opacity-80 mix-blend-screen">
        <img src="data:image/jpeg;base64,{encoded_string}" class="w-32" style="width: 140px; height: auto; filter: invert(1) brightness(1.5);">
        
        <div class="mt-2 font-handwriting text-slate-500 text-sm tracking-widest uppercase" style="font-family: 'Outfit', sans-serif; letter-spacing: 0.2em; font-size: 0.7rem;">
            Protik Chowdhury
        </div>
    </div>'''

        # We need to replace the EXISTING div.
        # It starts at <!-- Signature --> and ends at the next </div> </div> closure?
        # That's risky with regex.
        
        # Let's read the file line by line and replace the block.
        lines = content.split('\n')
        new_lines = []
        skip = False
        inserted = False
        
        for line in lines:
            if '<!-- Signature -->' in line:
                if not inserted:
                    new_lines.append(new_div)
                    inserted = True
                skip = True
            
            if skip:
                # We skip lines until we see the closing div of the signature block.
                # The signature block has outer div, img, inner div.
                # So we wait for the 2nd closing div? indentation is reliable here: "    </div>"
                if line.strip() == '</div>' and '    </div>' in line: 
                     # This logic is brittle. 
                     # Let's rely on the fact that we just added it at the end of body.
                     pass
            
            # Alternative: simpler string replace of the known truncated line?
            # The tool output showed: <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...
            # Let's just blindly replace the whole file content since I can't see the exact truncated line state easily.
            pass

        # Let's allow the user to see - we'll just rewrite the file intelligently.
        # We know the signature is at the bottom.
        # Let's remove the old signature block and append the new one before </body>
        
        clean_content = content.split('<!-- Signature -->')[0]
        # Check if we split correctly
        if len(clean_content) == len(content):
             print("Could not find <!-- Signature --> marker to replace.")
             return

        # Re-assemble
        final_content = clean_content + new_div + '\n</body>\n\n</html>'
        
        with open(html_path, 'w') as f:
            f.write(final_content)
            
        print("Successfully embedded full base64 signature.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    embed_signature()
