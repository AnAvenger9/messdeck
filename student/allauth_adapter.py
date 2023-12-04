from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        # Customize this function to filter users based on the email domain
        allowed_email_domain = 'pilani.bits-pilani.ac.in'  # Change this to your allowed domain
        user_email = sociallogin.account.extra_data.get('email', '')
        return user_email.endswith('@' + allowed_email_domain)