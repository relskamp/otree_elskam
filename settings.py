import os

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# OTREE_PRODUCTION just controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if os.environ.get('OTREE_PRODUCTION') in {None, '', '0'}:
    DEBUG = True
else:
    DEBUG = False

# IS_OTREE_DOT_ORG is only used on demo.otree.org.
# you can assume it is None/''/0.
if os.environ.get('IS_OTREE_DOT_ORG') in {None, '', '0'}:
    ADMIN_PASSWORD = 'otree'
    # don't share this with anybody.
    # Change this to something unique (e.g. mash your keyboard),
    # and then delete this comment.
    SECRET_KEY = 'zzzzzzzzzzzzzzzzzzzzzzzzzzz'
else:
    # ignore the next 2 lines;
    # only used on demo.otree.org
    ADMIN_PASSWORD = os.environ['OTREE_ADMIN_PASSWORD']
    SECRET_KEY = os.environ['OTREE_SECRET_KEY']

PAGE_FOOTER = ''

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}


ADMIN_USERNAME = 'admin'

# AUTH_LEVEL:
# If you are launching an experiment and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to EXPERIMENT.

# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = os.environ.get('OTREE_AUTH_LEVEL')

# ACCESS_CODE_FOR_DEFAULT_SESSION:
# If you have a "default session" set,
# then an access code will be appended to the URL for authentication.
# You can change this as frequently as you'd like,
# to prevent unauthorized server access.

ACCESS_CODE_FOR_DEFAULT_SESSION = 'my_access_code'

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False


# e.g. en-gb, de-de, it-it, fr-fr.
# see: https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'


APPS = [
    'otree',
    'django.contrib.humanize'
]

DEBUG_APPS = [
    "django_extensions"
]

INSTALLED_APPS = APPS + (DEBUG_APPS if DEBUG else [])


if 'SENTRY_DSN' in os.environ:
    INSTALLED_APPS += [
        'raven.contrib.django.raven_compat',
    ]

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            Source code
        </a> for the below games.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Below are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish to create your own variations.
    Click one to learn more and play.
</p>
"""

# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        qualification.LocaleRequirement("EqualTo", "US"),
        qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        #qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1,
    'participation_fee': 3,
    'num_bots': 12,
    'doc': "",
    'group_by_arrival_time': False,
    'mturk_hit_settings': mturk_hit_settings
}

SESSION_CONFIGS = [
    {
        'name': 'elskamp_auction_game',
        'display_name': "Demographic Questionaire",
        'num_demo_participants': 8,
        'app_sequence': [
            "questionnaire",
        ],
    },
                   
                 
    {
        'name': 'elskamp_auction_game_review_T1UA',
         'display_name': "Part1_T1UA",
         'num_demo_participants': 8,
         'app_sequence': [
           "review_questions_T1UA",],
          'treatment': "T1-UA",
    },

    {
        'name': 'elskamp_auction_game_review_T1DA',
        'display_name': "Part1_T1DA",
        'num_demo_participants': 8,
        'app_sequence': [
         "review_questions_T1DA",],
         'treatment': "T1-DA",
       },
                   
      {
    'name': 'elskamp_auction_game_review_T2UA',
    'display_name': "Part1_T2UA",
    'num_demo_participants': 8,
    'app_sequence': [
    "review_questions_T2UA",],
    'treatment': "T2-UA",
      },
                   
   {
   'name': 'elskamp_auction_game_review_T2DA',
    'display_name': "Part1_T2DA",
    'num_demo_participants': 8,
    'app_sequence': [
    "review_questions_T2DA",],
    'treatment': "T2-DA",
    },
                  
                                
                   
    {
        'name': 'elskamp_auction_game_t1_ua',
        'display_name': "Part2_ T1-UA",
        'num_demo_participants': 2,
        'app_sequence': ["auction"],
        'treatment': "T1-UA",
    },
    {
        'name': 'elskamp_auction_game_t1_da',
        'display_name': "Part2_T1-DA",
        'num_demo_participants': 2,
        'app_sequence': ["auction"],
        'treatment': "T1-DA",
    },
    {
        'name': 'elskamp_auction_game_t2_ua',
        'display_name': "Part2_T2-UA",
        'num_demo_participants': 3,
        'app_sequence': ["auction"],
        'treatment': "T2-UA",
    },
    {
        'name': 'elskamp_auction_game_t2_da',
        'display_name': "Part2_T2-DA",
        'num_demo_participants': 3,
        'app_sequence': ["auction"],
        'treatment': "T2-DA",
    },
]

otree.settings.augment_settings(globals())
