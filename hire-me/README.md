# Hire me

Static hiring page using the shared article layout and the previously unused coral floral theme. The original `china-vase-1-1600.jpg` download is already stored unchanged in `design/article-layout/coral/china-vase-1.jpg`. Source attribution is included on both pages.

## Email delivery

The HTML form posts directly to FormSubmit, forwarding enquiries to `tfothergill96@gmail.com`. There are no browser-side email credentials, dependencies or custom backend. FormSubmit supplies the spam check; the hidden honeypot provides an additional filter. Its `email` field sets Reply-To, and the table template includes all named fields. The direct email links work independently of the form service.

The first submission triggers a one-time activation email. The mailbox owner must activate the form before delivery works. After activation, send a fresh labelled test from the live page and verify receipt, Reply-To, all fields and the return to `/hire-me/thanks/`. A provider response alone does not prove inbox delivery. FormSubmit says it retains submissions for 30 days, including submissions pending activation.

The form uses normal browser validation and a standard POST, so it also works without JavaScript. The provider's spam-check page handles submission before redirecting to the absolute URL in `_next`. Local submission redirects to the live thank-you page intentionally; test the field validation and request payload locally with network interception to avoid sending test spam.

Provider documentation: https://formsubmit.co/documentation and https://formsubmit.co/help.

## Local verification

Checked the homepage, hiring page and thank-you page at 320, 390, 768, 1024 and 1440px with no horizontal overflow. Browser checks cover empty-form validation, invalid email rejection, required budget, a blank optional company, and an intercepted POST containing every enquiry field, Reply-To email, empty honeypot and the correct thank-you URL. Local links and pattern assets resolve. No email is sent by these intercepted tests; live activation and inbox receipt require separate verification.

To change the recipient, update the form action and direct email links, then activate the new address. Keep `_next` and `_url` aligned with the published site if the domain changes.
