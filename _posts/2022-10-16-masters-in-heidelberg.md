---
title: Master's in Heidelberg
category: "education"
category_icon: /assets/category-icons/heidelberg.webp
pdf: true
excerpt: Things we learned during our move to Heidelberg (Germany) for our master's degrees, including enrolment, housing, travel, torrenting, and more.
---

- .
{:toc}

I, along with my <a class='secret' href='/assets/kacka.webp'>lovely girlfriend</a>, recently moved to Heidelberg to pursue our respective master's degrees (Computer Science and Cancer Biology).
While Heidelberg is a beautiful city with great sights, interesting people and a pretty good bouldering gym, the process of becoming a European international student can be quite challenging.

If you find yourself in a similar position (or are considering placing yourself in it), I hope this post will be useful to you, since it covers a number of the things we struggled with during the enrolment process and beyond.

_Note: this post is ever-expanding. If you've also experienced some issues with education in Heidelberg, or have some experiences you'd like to share, please let me know and I'll add them here._


### Enrolment

#### Application
This step of the enrolment process can be either tedious (in the case of [Cancer Biology](https://www.uni-heidelberg.de/en/study/all-subjects/molecular-biosciences/molecular-biosciences-master)) or very straightforward (in the case of [Data and Computer Science](https://www.uni-heidelberg.de/en/study/all-subjects/applied-computer-science/data-and-computer-science-master)), depending entirely on your major.

In the former case, you have to
1. send in your CV and a motivation letter and, if chosen,
2. attend an interview with a presentation you prepared[^interview]

[^interview]: Interviewers are Faculty members from German Cancer Research Center (DKFZ) since this institute is closely connected with the major. The interview started with a 5-minute presentation given by the student. The topic could be the bachelor thesis or any other scientific project you did. After the presentation, the interviewer asked questions about the project presented, some fundamental knowledge of molecular biology, and motivation to study at Heidelberg University.

In the latter case, there was no interview so you could skip directly to sending the application documents (required by both).
This includes (but is not limited to):
- a filled-in **application**,
- a certificate of **English proficiency** (at least B2)[^german]
- a transcript of **completed study requirements** (I haven't received my degree at a time),
- a certified copy of a **high-school diploma** and
- a copy of my **ID** (or a VISA, if you're not a European citizen).

[^german]: If it's a German master's degree, you'll need a certificate of German proficiency instead.

Once the admissions are opened (~March 2022 for our programmes), the specific list will be at the respective degree's website.
You might have to do a little bit of digging and translating, though (the study requirements might be in German even if the degree isn't).

Sending the documents by post is best done by private carriers such as [UPS](https://www.ups.com/us/en/global.page) instead of the post, because they're faster, more liable and will notify you when the documents arrived, albeit a little more costly (~€30 from the Czech Republic).


#### Immatriculation

Once you have been accepted and have received your letter of admission, you will know what other documents the university requires to finish your enrolment.
This can vary quite drastically between the degrees, what was required for Computer Science was
- a filled-in **application for immatriculation**[^address],
- a **university diploma** or a **final transcript** of my home university,
- a **passport-size photo** (35mm \(\times\) 45mm),
- **proof of health insurance**[^insurance],
- **proof of finance** ([this document](/assets/masters-in-heidelberg/proof-of-finance.pdf)) and
- a copy of my **ID** (again, or a VISA for non-EU citizens).

[^address]: If you don't have a German address, just write something like _Documents will be picked up in person_ in the "Temporary residence in Germany" section and pick them up when you arrive in Heidelberg, else they will send them by post and it could take a **very** long time (much longer than the start of classes).

[^insurance]: This was a bit tricky. If you're outside of the EU, you'll need to contact an insurance provider in Germany. If you're from the EU, you most likely have a EHIC-compliant insurance card. **It is not enough to send a copy** as the university requires that a German insurance provider confirms the validity of the card. This was, however, relatively easy, as described in [this document](/assets/masters-in-heidelberg/insurance.pdf).

After everything has been sent, you'll need to wait a bit (say a week) and then pick up your documents (ID, Matriculation documents, etc.) from [this building](https://goo.gl/maps/LtnHGVDei4EtHR719).
There are some more steps afterwards, such as
- activating your student ID,
- paying the student fee[^fee],
- setting up [Eduroam](https://www.urz.uni-heidelberg.de/en/service-catalogue/network/wi-fi-via-eduroam),
- browsing [IT services](https://www.urz.uni-heidelberg.de/en/support/it-for-all-target-groups/it-for-students) such as [VPN](https://www.urz.uni-heidelberg.de/en/service-catalogue/network/vpn-virtual-private-network) or [printing](https://www.urz.uni-heidelberg.de/en/service-catalogue/printing/public-printers-and-copiers) and
- checking your [email](https://sogo02.urz.uni-heidelberg.de/SOGo/),

but they are well-described in the documents you receive so I won't cover them here.

[^fee]: This again depends on whether you're a citizen of EU (the fee is pretty small, we payed ~€170) or not (the fee is substantial large). In any case, the payment can take a little while to confirm (at least when paying from Revolut), so don't panic.

#### Email Client Setup

Adding this section since I had to do this multiple times and mess it up everytime (the [online documentation](https://www.urz.uni-heidelberg.de/en/service-catalogue/email-and-groupware/email-server) is not entirely well written).
The configuration for me (Tomáš Sláma, `tm304`) is the following:

```yaml
Address: tomas.slama@stud.uni-heidelberg.de

Incomming: # IMAP
    Hostname: imap.urz.uni-heidelberg.de
    Port: 143 # STARTTLS
    Username: tm304

Outgoing: # SMTP
    Hostname: mail.urz.uni-heidelberg.de
    Port: 587 # STARTTLS
    Username: tm304
```

**Note that sending email doesn't work from other countries. Use a VPN!**

### Money
If Euros aren't your nation's currency (which was the case for me as we use Czech Korunas), there is a chance that paying using your bank's card will include additional fees and unfavorable conversion rates of your central bank.
If that is the case, it might be advisable to either
- set-up an account at a German bank or
- use a service like [Revolut](https://www.revolut.com/) that facilitate currency conversions without additional fees[^revolut].

[^revolut]: As of 11/2022, Revolut allows free monthly conversions of around €1000, if you don't have a premium account. This will most likely be enough for you, depending on your housing and lifestyle.

I've chosen to use Revolut and it has been working well so far -- the app is easy to use, the money easy to track and the card has been working fine without any issues.
If you'd like to try it too, **let someone who already has Revolut know[^noone]** since they could invite you through Revolut's referral programme and receive some money for free.

[^noone]: If you don't know anyone and would like to help me out, let me know.

Getting either of those is also quite important for signing up for services memberships for places like the Boulderhaus, [getting a German phone number](https://www.expatica.com/de/living/household/german-sim-card-244240/) or even paying rent, since a lot of them use **direct debit** -- if you don't do so, make sure your bank supports this type of payment.

Also, most places in Heidelberg accept cards, so you don't need to have a lot of cash on-hand.


### Housing
It's fucked up.

Your best bet is to start **really** early and try to apply for housing in Heidelberg's dorms (via [student union](https://stw.uni-heidelberg.de/en/) or privately-owned).
If they're full, going in person and making sad eyes reportedly works, although I haven't tried.
You should also try to periodically scour [wg-gesucht](https://wg-gesucht.de/), which is targeted at student housing -- this is how we got our appartment.
**Do not use [immobilienscout24](https://www.immobilienscout24.de/)** as they are an absolutely awful company, with most of the properties being spam or automated posts linking to the websites of other companies (not to mention their predatory Plus account).

The text we usually sent, along with a **SCHUFA certificate** (which you can either buy or can actually get for free if you do some due diligence and are not as pressed for time as we were) is the following, both in English and in German:

<!---MARKDOWN-->

<details>
	<summary>English</summary>
	<div markdown="1">
> Greetings,
>
> me and my girlfriend (both 22 years old) are starting our Master's degrees in Heidelberg and would be interested in the apartment. I will be studying Computer Science and she will be studying Cancer Biology. Since the semester starts quite soon, we'd like to move in as soon as possible, but the date is very much flexible.
>
> We're both from the Czech Republic and have been together for 8 years now. We're quiet and not very outgoing, mostly focusing on our studies and hobbies (rock climbing, dance). We don't smoke and have no pets.
>
> In terms of financing, we are fortunate to have the financial support of both of our parents, along with having a sizable amount of savings.
>
> If you think we'd be the right fit for the apartment, please let me know either through the website or by email (tomas@slama.dev) or phone (my phone number).
>
> Have a nice day and thank you in advance!
>
> Sincerely
> T. Sláma
</div>
</details>

<!---PDF

> Greetings,
>
> me and my girlfriend (both 22 years old) are starting our Master's degrees in Heidelberg and would be interested in the apartment. I will be studying Computer Science and she will be studying Cancer Biology. Since the semester starts quite soon, we'd like to move in as soon as possible, but the date is very much flexible.
>
> We're both from the Czech Republic and have been together for 8 years now. We're quiet and not very outgoing, mostly focusing on our studies and hobbies (rock climbing, dance). We don't smoke and have no pets.
>
> In terms of financing, we are fortunate to have the financial support of both of our parents, along with having a sizable amount of savings.
>
> If you think we'd be the right fit for the apartment, please let me know either through the website or by email (tomas@slama.dev) or phone (my phone number).
>
> Have a nice day and thank you in advance!
>
> Sincerely
> T. Sláma
-->

<!---MARKDOWN-->
<!---PDF
---
-->

<!---MARKDOWN-->
<details>
	<summary>German</summary>
	<div markdown="1">
> Schöne Grüße,
>
> ich und meine Freundin (beide 22 Jahre alt) beginnen unser Masterstudium in Heidelberg und hätten Interesse an der Wohnung. Ich werde Informatik studieren und sie wird Krebsbiologie studieren. Da das Semester ziemlich bald beginnt, würden wir gerne so schnell wie möglich einziehen, aber der Termin ist sehr flexibel.
>
> Wir kommen beide aus Tschechien und sind jetzt seit 8 Jahren zusammen. Wir sind ruhig und nicht sehr kontaktfreudig und konzentrieren uns hauptsächlich auf unser Studium und unsere Hobbys (Klettern, Tanzen). Wir rauchen nicht und haben keine Haustiere.
>
> In Bezug auf die Finanzierung haben wir das Glück, die finanzielle Unterstützung unserer beiden Eltern zu haben, zusammen mit einer beträchtlichen Summe an Ersparnissen.
>
> Wenn Sie der Meinung sind, dass wir für die Wohnung geeignet sind, lassen Sie es mich bitte entweder über die Website oder per E-Mail (tomas@slama.dev) oder Telefon (Meine Telefonnummer) wissen.
>
> Schönen Tag noch und danke im Voraus!
>
> Aufrichtig
> T. Sláma
</div>
</details>

<!---PDF

> Schöne Grüße,
>
> ich und meine Freundin (beide 22 Jahre alt) beginnen unser Masterstudium in Heidelberg und hätten Interesse an der Wohnung. Ich werde Informatik studieren und sie wird Krebsbiologie studieren. Da das Semester ziemlich bald beginnt, würden wir gerne so schnell wie möglich einziehen, aber der Termin ist sehr flexibel.
>
> Wir kommen beide aus Tschechien und sind jetzt seit 8 Jahren zusammen. Wir sind ruhig und nicht sehr kontaktfreudig und konzentrieren uns hauptsächlich auf unser Studium und unsere Hobbys (Klettern, Tanzen). Wir rauchen nicht und haben keine Haustiere.
>
> In Bezug auf die Finanzierung haben wir das Glück, die finanzielle Unterstützung unserer beiden Eltern zu haben, zusammen mit einer beträchtlichen Summe an Ersparnissen.
>
> Wenn Sie der Meinung sind, dass wir für die Wohnung geeignet sind, lassen Sie es mich bitte entweder über die Website oder per E-Mail (tomas@slama.dev) oder Telefon (Meine Telefonnummer) wissen.
>
> Schönen Tag noch und danke im Voraus!
>
> Aufrichtig
> T. Sláma

-->


### Travel
This depends a lot on where you live but it might be a good idea to purchase the [Semester Ticket](https://www.uni-heidelberg.de/en/study/management-of-studies/tuition-fees/semester-ticket-for-public-transportation), which allows you to use pretty much[^noice] any public transport in the [Rhein-Neckar region](/assets/masters-in-heidelberg/rhein-neckar-region.webp), which includes Heidelberg, Mannheim and the surrounding towns.

[^noice]: This excludes high-speed trains (like ICE).

Also, if you can, travel by bike.
Heidelberg is made for travel by bike -- it has great infrastructure (bike lanes and racks everywhere), cars are used to them and it is arguably the fastest way to travel here since the public transport always has delays.

If you don't own a bike, use a bike-sharing service like [nextbike](https://www.vrnnextbike.de/en/heidelberg/), which allows up to 30 minutes of free travel _per rental_ (for students).
This is likely more than enough time to travel from/to any campus/mensa during your daily schedule.

For traveling to specific campus buildings, here are some very useful maps for each campus part ([Altstadt](/assets/masters-in-heidelberg/altstadt.pdf), [Bergheim](/assets/masters-in-heidelberg/bergheim.pdf) and [Im Neuenheimer Feld](/assets/masters-in-heidelberg/im-neuenheimer-feld.pdf)).


### Dining

There are a [number of mensas](https://www.studentenwerk.uni-heidelberg.de/en/mensen_neu) in Heidelberg, the most frequented being the [Zentralmensa](https://www.studentenwerk.uni-heidelberg.de/en/node/344).
They provide food both as a **buffet** (which is great because you can regulate how much you eat) and **ready meals** (which are slightly cheaper but uniform).

My favorite is the [Zeughaus Mensa](https://www.studentenwerk.uni-heidelberg.de/en/node/342) near Universitätsplatz, which always has excellent food, along with a café (with student prices).
The best thing is that it closes pretty late (9 PM) and is also open on Saturday, so you can really minimize the amount you cook, if you're not into that or don't have the facilities at home.


### Education

The structure of your degree varies drastically from degree to degree.
Some programmes have a relatively predetermined schedule, while others are more open.

One thing that is a constant in all of this is [LSF](https://lsf.uni-heidelberg.de/), which is the central platform for organizing your education in Heidelberg.
After reading through the handbook for your respective Master's degree, you should find the courses you'd like to sign up for in the course catalogue.
For each course, there is usually a sign-up link, leading to one of the many e-learning platforms used ([Müsli](https://muesli.mathi.uni-heidelberg.de/), [Moodle](https://moodle.uni-heidelberg.de/login/index.php), [Mampf](https://mampf.mathi.uni-heidelberg.de/), etc.).


### Torrenting

**Don't torrent without a VPN. Seriously.**

You will receive a warning and will have to pay (either a lot directly or a little less when going through a mediation company).
If this has already happened, [read this article](https://www.settle-in-berlin.com/illegal-file-sharing-germany-letter-cease-desist-warning/) and follow the advice.

I'm adding this here since Germany's stance to torrenting is quite different (there is a whole industry around this) to that of some other European countries and might catch you off guard like it did us.
It is absolutely nonsensical and predatory, but unfortunately not much can be done.
