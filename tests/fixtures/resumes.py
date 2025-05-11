# tests/fixtures/resumes.py
from datetime import datetime
import pytz
from src.core.domain.resume import Resume, Experience, ContactInfo, Education

def create_alfred_pennyworth_resume():
    """
    Create Alfred Pennyworth's resume sample for testing.
    
    :return: A fully populated Resume object
    :rtype: Resume
    """
    return Resume(
        contact_info=ContactInfo(
            name='Alfred Pennyworth',
            email='alfred.pennyworth@email.com',
            phone='(123) 456-7890',
            location='Silicon Valley, CA, USA',
            links=['apennyworth']
        ),
        summary='Seasoned Product Manager with over 20 years of experience in software development and product management, having worked at all FAANG companies. Exceptional leadership skills, strategic thinking, and a track record of managing products from conception to market success.',
        experiences=[
            Experience(
                title='Product Manager',
                company='Google',
                start_date=datetime(2017, 1, 1, tzinfo=pytz.UTC),
                end_date=None,  # Current job
                description=[
                    'Leading cross-functional teams to design, develop, and launch innovative products.',
                    'Developing product strategies and making data-driven decisions to improve user experience and meet business goals.'
                ],
                achievements=[]
            ),
            Experience(
                title='Software Development Engineer III',
                company='Amazon',
                start_date=datetime(2012, 1, 1, tzinfo=pytz.UTC),
                end_date=datetime(2017, 1, 1, tzinfo=pytz.UTC),
                description=[
                    'Led a team of developers in building scalable and high-performing e-commerce applications.',
                    'Successfully delivered multiple projects within the stipulated time and budget.'
                ],
                achievements=[]
            ),
            Experience(
                title='Software Development Engineer II',
                company='Apple',
                start_date=datetime(2007, 1, 1, tzinfo=pytz.UTC),
                end_date=datetime(2012, 1, 1, tzinfo=pytz.UTC),
                description=[
                    'Designed and implemented software components for various Apple services.',
                    'Optimized the performance of applications and improved code quality through thorough testing.'
                ],
                achievements=[]
            ),
            Experience(
                title='Software Development Engineer I',
                company='Netflix',
                start_date=datetime(2002, 1, 1, tzinfo=pytz.UTC),
                end_date=datetime(2007, 1, 1, tzinfo=pytz.UTC),
                description=[
                    'Developed and maintained the user interface for the Netflix web application.',
                    'Worked closely with product managers and designers to create an optimal user experience.'
                ],
                achievements=[]
            ),
            Experience(
                title='Software Development Engineer I',
                company='Facebook',
                start_date=datetime(1999, 1, 1, tzinfo=pytz.UTC),
                end_date=datetime(2002, 1, 1, tzinfo=pytz.UTC),
                description=[
                    'Played a key role in the development of early Facebook features.',
                    'Implemented scalable back-end services using Java and SQL.'
                ],
                achievements=[]
            )
        ],
        education=[
            Education(
                degree='Master of Business Administration',
                institution='Stanford University',
                graduation_date=datetime(2018, 1, 1, tzinfo=pytz.UTC),
                gpa=None,
                highlights=[]
            ),
            Education(
                degree='Master of Science in Computer Science',
                institution='Massachusetts Institute of Technology',
                graduation_date=datetime(1999, 1, 1, tzinfo=pytz.UTC),
                gpa=None,
                highlights=[]
            ),
            Education(
                degree='Bachelor of Science in Computer Science',
                institution='University of California, Berkeley',
                graduation_date=datetime(1997, 1, 1, tzinfo=pytz.UTC),
                gpa=None,
                highlights=[]
            )
        ],
        skills=[
            'Product management',
            'Agile methodologies',
            'Leadership',
            'Communication',
            'Project management',
            'User Experience Design',
            'Market Research',
            'Data Analysis',
            'Java',
            'Python',
            'JavaScript',
            'HTML/CSS',
            'SQL',
            'AWS'
        ],
        certifications=[],
        achievements=[],
        publications=[]
    )

def create_bruce_wayne_resume():
    """
    Create Bruce Wayne's resume sample for testing.
    
    :return: A fully populated Resume object
    :rtype: Resume
    """
    return Resume(
        contact_info=ContactInfo(
            name='Bruce Wayne',
            email='bruce.wayne@wayneenterprises.com',
            phone='(555) 123-4567',
            location='Gotham City, USA',
            links=['linkedin.com/in/brucewayne', 'github.com/not-batman']
        ),
        summary='Innovative tech executive with 15+ years of experience leading teams and driving organizational growth. Strong background in AI, cybersecurity, and sustainable technology solutions. Expert in strategic planning and turning around underperforming operations.',
        experiences=[
            Experience(
                title='Chief Technology Officer',
                company='Wayne Enterprises',
                start_date=datetime(2015, 3, 1, tzinfo=pytz.UTC),
                end_date=None,  # Current job
                description=[
                    'Oversee all technology initiatives and R&D projects with a $500M annual budget',
                    'Lead digital transformation initiatives across 7 subsidiary companies',
                    'Develop and implement enterprise-wide cybersecurity protocols'
                ],
                achievements=[
                    'Increased operational efficiency by 35% through strategic AI implementation',
                    'Reduced security incidents by 78% through enhanced system architecture',
                    'Launched 5 successful tech products generating $1.2B in new revenue'
                ]
            ),
            Experience(
                title='Director of Research & Development',
                company='Wayne Technologies',
                start_date=datetime(2010, 6, 1, tzinfo=pytz.UTC),
                end_date=datetime(2015, 2, 28, tzinfo=pytz.UTC),
                description=[
                    'Managed a team of 120 scientists and engineers working on cutting-edge technologies',
                    'Directed projects in renewable energy, advanced materials, and computer vision',
                    'Established partnerships with leading universities and research institutions'
                ],
                achievements=[
                    'Developed patented graphene-based material with applications in defense and construction',
                    'Secured $45M in government research grants',
                    'Created an AI-based surveillance system with 99.8% accuracy in threat detection'
                ]
            ),
            Experience(
                title='Lead Engineer',
                company='LexCorp',
                start_date=datetime(2005, 9, 1, tzinfo=pytz.UTC),
                end_date=datetime(2010, 5, 31, tzinfo=pytz.UTC),
                description=[
                    'Led engineering team designing advanced defense systems',
                    'Coordinated with military contractors on classified projects',
                    'Implemented rigorous quality control and testing procedures'
                ],
                achievements=[
                    'Successfully delivered projects 15% under budget and ahead of schedule',
                    'Recognized with LexCorp Innovation Award for breakthrough in materials science',
                    'Mentored 20+ junior engineers, with 80% achieving promotions within 3 years'
                ]
            )
        ],
        education=[
            Education(
                degree='MBA',
                institution='Gotham University',
                graduation_date=datetime(2008, 5, 15, tzinfo=pytz.UTC),
                gpa=4.0,
                highlights=['Graduated with highest honors', 'Specialization in Technology Management']
            ),
            Education(
                degree='Master of Science in Computer Engineering',
                institution='Massachusetts Institute of Technology',
                graduation_date=datetime(2005, 5, 20, tzinfo=pytz.UTC),
                gpa=3.95,
                highlights=['Thesis on advanced encryption algorithms', 'Presidential Fellowship recipient']
            ),
            Education(
                degree='Bachelor of Science in Physics',
                institution='Princeton University',
                graduation_date=datetime(2003, 5, 25, tzinfo=pytz.UTC),
                gpa=3.9,
                highlights=['Summa Cum Laude', 'Senior thesis on quantum computing applications']
            )
        ],
        skills=[
            'Strategic Leadership',
            'Artificial Intelligence',
            'Machine Learning',
            'Cybersecurity',
            'R&D Management',
            'Product Development',
            'Quantum Computing',
            'Python',
            'C++',
            'TensorFlow',
            'System Architecture',
            'Blockchain',
            'Renewable Energy',
            'Materials Science',
            'Team Leadership'
        ],
        certifications=[
            'Certified Information Systems Security Professional (CISSP)',
            'Project Management Professional (PMP)',
            'AWS Certified Solutions Architect',
            'Chartered Financial Analyst (CFA)'
        ],
        achievements=[
            'Named "Top 40 Under 40" by Gotham Business Journal (2018)',
            'Holds 28 patents in advanced materials and security technologies',
            'Board member, Gotham Technology Initiative (2016-Present)',
            'Established Wayne Foundation Technology Scholarship (funds 50 STEM students annually)'
        ],
        publications=[
            'Wayne, B. (2020). "Quantum Encryption: The Future of Secure Communications." Journal of Cybersecurity Advances.',
            'Wayne, B. (2019). "Applications of Graphene in Next-Generation Computing." Materials Science Quarterly.',
            'Wayne, B. (2017). "Ethical Considerations in AI Development." Tech Ethics Review.'
        ]
    )

def get_all_sample_resumes():
    """
    Return a dictionary of all sample resumes.
    
    :return: Dictionary mapping names to Resume objects
    :rtype: Dict[str, Resume]
    """
    return {
        "alfred_pennyworth": create_alfred_pennyworth_resume(),
        "bruce_wayne": create_bruce_wayne_resume()
    }