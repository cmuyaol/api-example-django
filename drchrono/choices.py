gender_choices = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)

race_choices = (
    ("blank", ""),
    ("indian", "indian"),
    ("asian", "asian"),
    ("black", "black"),
    ("hawaiian", "hawaiian"),
    ("white", "white"),
    ("declined", "declined")
)

ethnicity_choices = (
    ("blank", ""),
    ("hispanic", "Hispanic or Latino"),
    ("not_hispanic", "Not Hispanic or Latino"),
    ("declined", "Declined to specify")
)
preferred_language_choices = (
    ("eng", "English"),
    ("chi", "Chinese"),
    ("fre", "French"),
    ("ita", "Italian"),
    ("jpn", "Japanese"),
    ("por", "Portuguese"),
    ("rus", "Russian"),
    ("spa", "Spanish; Castilian"),
    ("1", "Other"),
    ("2", "Unknown"),
    ("3", "Declined to specify"),

)

patient_student_status_choices = (
    ("E", "Employed"),
    ("F", "Full-time student"),
    ("N", "Not a Student"),
    ('P', "Part-time Student")
)

state_choices = (('AL', 'Alabama'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
                 ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'),
                 ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'),
                 ('GA', 'Georgia'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'),
                 ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'),
                 ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'),
                 ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
                 ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
                 ('NC', 'North Carolina'),('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'),
                 ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
                 ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'),
                 ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')
)
#
# patient_martial_status_choices = (
#     "Married",
#     "Single",
#     "Widowed",
#     "Divorced",
#     "Other"
# )
#
# EPSDT_services_choices = (
#     "Children",
#     "Family Planning",
#     "Children / Family Planning",
#     "Pregnancy"
# )

appointment_status_choices = (
    "Arrived",
    "Checked In",
    "In Room",
    "Cancelled",
    "Complete",
    "Confirmed",
    "In Session",
    "No Show",
    "Not Confirmed",
    "Rescheduled"
)