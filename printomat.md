---
title: Printomat
layout: default
no-heading: True
icon: fa-print
css: printomat
htmx: true
---

Send me a message that will get printed on my home receipt printer.

<form id="printForm" hx-post="https://printomat.slama.dev/submit" hx-target="#printForm" hx-swap="outerHTML"  hx-request="true">
    <fieldset>
        <div>
            <label for="content"><strong>Message</strong></label>
            <textarea id="message" name="message" placeholder="Enter the content you want to print..."></textarea>
        </div>

        <div>
            <label for="imageFile"><strong>Image</strong></label>
            <div class="image-input-group">
                <input type="file" id="imageFile" name="imageFile" accept="image/png" onchange="handleImageSelect(event)">
                <button type="button" onclick="clearImage()">Clear</button>
            </div>
            <input type="hidden" id="image" name="image">
        </div>

        <div class="inline-input">
            <label for="token"><strong>Friendship Token</strong>:</label>
            <input type="text" id="token" name="token" placeholder="Enter a token if you have one...">
        </div>

        <div>
            <button type="submit">Submit</button>
        </div>
    </fieldset>
</form>

<script>
function handleImageSelect(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function() {
        document.getElementById('image').value = reader.result.split(',')[1];
    };
    reader.readAsDataURL(file);
}

function clearImage() {
    document.getElementById('imageFile').value = '';
    document.getElementById('image').value = '';
}
</script>
