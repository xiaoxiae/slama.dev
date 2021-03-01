#!/usr/bin/env python3

import string
import os

rick = """
We're no strangers to love

You know the rules and so do I
A full commitment's what I'm thinking of
You wouldn't get this from any other guy
I just wanna tell you how I'm feeling

Gotta make you understand

Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye

Never gonna tell a lie and hurt you
We've known each other for so long
Your heart's been aching but
You're too shy to say it
Inside we both know what's been going on

We know the game and we're gonna play it
And if you ask me how I'm feeling
Don't tell me you're too blind to see
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you

Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you

Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you

Never gonna give, never gonna give

Never gonna give, never gonna give

We've know each other for so long
Your heart's been aching but
You're too shy to say it
Inside we both know what's been going on

We know the game and we're gonna play it
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up

Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
""".lower()

songs = """
- America -- A Horse With No Name
- Beatles -- Come Together
- Beatles -- Lucy In The Sky With Diamonds
- Billy Joel -- Movin' Out
- Billy Joel -- Piano Man
- Black Sabbath -- War Pigs
- Blue Oyster Cult -- (Don't Fear) The Reaper
- Blue Oyster Cult -- Burnin' For You
- Blue Swede -- Hooked on a Feeling
- Bob Dylan -- Knockin' On Heaven's Door
- Bob Dylan -- Mr. Tambourine Man
- Boston -- Long Time
- Boston -- More Than A Feeling
- Boston -- Peace of Mind
- Cage The Elephant -- Ain't No Rest For The Wicked
- Cage The Elephant -- Come A Little Closer
- Cat Stevens -- Father and Son
- Cat Stevens -- Peace Train
- Cream -- White Room
- Creedence Clearwater Revival -- Bad Moon Rising
- Creedence Clearwater Revival -- Fortunate Son
- Creedence Clearwater Revival -- Green River
- Creedence Clearwater Revival -- Have You Ever Seen The Rain
- Creedence Clearwater Revival -- I Heard It Through The Grapevine
- David Bowie -- Life On Mars
- David Bowie -- Space Oddity
- David Bowie -- Starman
- Derek and the Dominos -- Layla
- Dire Straits -- Money For Nothing
- Dire Straits -- Sultans Of Swing
- Don McLean -- American Pie
- Earth, Wind & Fire -- Boogie Wonderland
- Earth, Wind & Fire -- September
- Electric Light Orchestra -- Mr. Blue Sky
- Elton John -- Rocket Man
- Fleetwood Mac -- Go Your Own Way
- Fleetwood Mac -- The Chain
- George Baker -- Little Green Bag
- George Harrison -- My Sweet Lord
- Glen Campbell -- Southern Nights
- Guns n' Roses -- Paradise City
- Herman's Hermits -- No Milk Today
- Jackson 5 -- I Want You Back
- Jay & The Americans -- Come A Little Bit Closer
- Johnny Cash -- God's Gonna Cut You Down
- Journey -- Don't Stop Believin'
- Kansas -- Carry on Wayward Son
- Kansas -- Dust in the Wind
- King Harvest -- Dancing In The Moonlight
- Led Zeppelin -- Black Dog
- Led Zeppelin -- Kashmir
- Led Zeppelin -- Stairway To Heaven
- Looking Glass -- Brandy
- Lynyrd Skynyrd -- Free Bird
- Lynyrd Skynyrd -- Simple Man
- Lynyrd Skynyrd -- Sweet Home Alabama
- Manfred Mann's Earth Band -- Blinded by the Light
- Marvin Gaye & Tammi Terrell -- Ain't No Mountain High Enough
- Men At Work -- Down Under
- Metallica -- Enter Sandman
- Muse -- Knights of Cydonia
- Neil Diamond -- Sweet Caroline
- Nirvana -- Smells Like Teen Spirit
- Oasis -- Wonderwall
- Pink Floyd -- Another Brick in the Wall
- Pink Floyd -- Comfortably numb
- Pink Floyd -- High Hopes
- Pink Floyd -- Wish You Were Here
- Punch Brothers -- Icarus Smicarus
- Queen -- Another One Bites The Dust
- Queen -- Bohemian Rhapsody
- Queen -- Heaven For Everyone
- Queen -- Keep Yourself Alive
- Queen -- Killer Queen
- Queen -- Mustapha
- Queen -- Seven Seas Of Rhye
- Queen -- Under Pressure
- Ram Jam -- Black Betty
- Redbone -- Come and Get Your Love
- Rupert Holmes -- Escape
- Silver -- Wham Bam Shang-A-Lang
- Simon & Garfunkel -- Mrs. Robinson
- Simon & Garfunkel -- The Boxer
- Simon & Garfunkel -- The Sound of Silence
- Stealers Wheel -- Stuck In The Middle With You
- Steppenwolf -- Born To Be Wild
- Steve Miller Band -- Jet Airliner
- Steve Miller Band -- Rock 'N Me
- Stevie Wonder -- Sir Duke
- Stevie Wonder -- Superstition
- Styx -- Renegade
- Sweet -- Fox On The Run
- Sweet -- The Ballroom Blitz
- The Animals -- The House of the Rising Sun
- The Clash -- Should I Stay or Should I Go
- The Eagles -- Hotel California
- The Handsome Family -- Far From Any Road
- The Mamas & the Papas -- California Dreamin'
- The Proclaimers -- I'm Gonna Be
- The Rolling Stones -- (I Can't Get No) Satisfaction
- The Rolling Stones -- Miss You
- The Rolling Stones -- Paint It, Black
- The Rolling Stones -- Sympathy For The Devil
- The White Strapes -- Apple Blossom
- The Who -- Baba O'riley
- Toto -- Africa
- Toto -- Hold The Line
- Trinity -- Annibale E I Cantori Moderni
- Turtles -- Happy Together
- Van Morrison -- Brown Eyed Girl
"""

rick_index = 0

base = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(base, "../_includes/songs.md"), "w") as f:
    for char in songs:
        while rick[rick_index] not in string.ascii_lowercase:
            rick_index += 1

        if char.lower() == rick[rick_index]:
            f.write(f"**{char}**")
            rick_index += 1
        else:
            f.write(char)

print("Rick-rolled!")
