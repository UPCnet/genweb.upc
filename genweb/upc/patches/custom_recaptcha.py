from genweb.core.utils import pref_lang
from plone.formwidget.recaptcha.view import IRecaptchaInfo
from recaptcha.client.captcha import displayhtml


def image_tag(self):
    lang = pref_lang()
    options = {"ca": """
                        <script type="text/javascript">
                            var RecaptchaOptions = {
                                    custom_translations : {
                                            instructions_visual : "Escriu les dues paraules:",
                                            instructions_audio : "Transcriu el que sentis:",
                                            play_again : "Torna a escoltar l'\u00e0udio",
                                            cant_hear_this : "Descarrega la pista en MP3",
                                            visual_challenge : "Modalitat visual",
                                            audio_challenge : "Modalitat auditiva",
                                            refresh_btn : "Demana dues noves paraules",
                                            help_btn : "Ajuda",
                                            incorrect_try_again : "Incorrecte. Torna-ho a provar.",
                                    },
                                    lang : '%s',
                                    theme : 'clean'
                                };
                        </script>
                        """ % lang,
               "es": """
                        <script type="text/javascript">
                            var RecaptchaOptions = {
                                    lang : '%s',
                                    theme : 'clean'
                            };
                        </script>
                        """ % lang,
               "en": """
                        <script type="text/javascript">
                            var RecaptchaOptions = {
                                    lang : '%s',
                                    theme : 'clean'
                            };
                        </script>
                        """ % lang
               }

    if not self.settings.public_key:
        raise ValueError, 'No recaptcha public key configured. Go to path/to/site/@@recaptcha-settings to configure.'
    use_ssl = self.request['SERVER_URL'].startswith('https://')
    error = IRecaptchaInfo(self.request).error
    return options.get(lang, '') + displayhtml(self.settings.public_key, use_ssl=use_ssl, error=error)
