---
title: Printomat
layout: default
icon: fa-print
htmx: true
---


Send me a message that will get [printed on my home receipt printer](https://github.com/xiaoxiae/Printomat/). No, I'm not kidding.

{{< photo_section caption="The printer in action - prints text, images, and occasionally bugs." >}}
{{< photo_row "printer-1.webp :: Receipt printer with a sample print. | printer-2.webp :: Receipt printer with a sample print. | printer-3.webp :: Receipt printer with a sample print." >}}
{{< /photo_section >}}

### Send a message!

<form id="printForm" hx-post="https://printomat.slama.dev/submit" hx-target="#printForm" hx-swap="outerHTML" hx-request="true">
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
<p class="small"><em>While I have implemented detections on both the server request side (timeouts, sane defaults) and the client side (hard limits on print frequency), it is possible for a motivated attacker to bypass those.
In that case, the worst thing that can happen is that there will be a stack of paper at my desk in the morning, a scowl on my face, and a swift disappearance of this fun project from my website.
<strong>Don't be a jerk</strong>.</em></p>
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
