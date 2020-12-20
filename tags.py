from PyPDF2 import PdfFileReader
import PyPDF2
import argparse
import io
import json
import os

import fitz # PyMuPDF
import io
from PIL import Image

from google.cloud import language_v1
from google.cloud import vision
import numpy
import six

def classify_text(tags_dict, text):
    language_client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    # Google API reads data
    response = language_client.classify_text(request={'document': document})
    categories = response.categories

    for category in categories:
        # if category.confidence >= 0.7:
        #     print("LARGE CONFIDENCE")
        # splits category name into subcategories
        category_arr = category.name.split("/")

        # Takes the max confidence of that category type
        if category_arr[-1] not in tags_dict.keys():
            tags_dict[category_arr[-1]] = round(category.confidence, 3)
        else:
            tags_dict[category_arr[-1]] = max(tags_dict[category_arr[-1]], round(category.confidence, 3))
    
    # debug
    if True:
        for category in categories:
            print(u"=" * 20)
            print(category.name, round(category.confidence, 3))
    return tags_dict

# generates category tags based on text file
def generate_tags_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        tags_dict = {}
        number_of_pages = pdf.getNumPages()
        for a in range(number_of_pages):
            page = pdf.getPage(a)
            text = page.extractText()
            text = text.split(". ")
            sentences = ""
            i = 0
            # generates category tag for text length ~300
            while i < len(text):
                sentences = ""
                while len(sentences) < 300 and i < len(text):
                    sentences += text[i]
                    i += 1
                if len(sentences) >= 175:
                    tags_dict = classify_text(tags_dict, sentences)
        # print(tags_dict)

def generate_tags_image(png_path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(png_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if False:
        for text in texts:
            print('\n"{}"'.format(text.description))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    all_text = ""
    for text in texts:
        all_text += " " + text.description

    return classify_text({}, all_text)

def create_tag_arr():
    category_arr = [
        "/Adult",
        "/Arts & Entertainment",
        "/Arts & Entertainment/Celebrities & Entertainment News",
        "/Arts & Entertainment/Comics & Animation",
        "/Arts & Entertainment/Comics & Animation/Anime & Manga",
        "/Arts & Entertainment/Comics & Animation/Cartoons",
        "/Arts & Entertainment/Comics & Animation/Comics",
        "/Arts & Entertainment/Entertainment Industry",
        "/Arts & Entertainment/Entertainment Industry/Film & TV Industry",
        "/Arts & Entertainment/Entertainment Industry/Recording Industry",
        "/Arts & Entertainment/Events & Listings",
        "/Arts & Entertainment/Events & Listings/Bars, Clubs & Nightlife",
        "/Arts & Entertainment/Events & Listings/Concerts & Music Festivals",
        "/Arts & Entertainment/Events & Listings/Expos & Conventions",
        "/Arts & Entertainment/Events & Listings/Film Festivals",
        "/Arts & Entertainment/Events & Listings/Movie Listings & Theater Showtimes",
        "/Arts & Entertainment/Fun & Trivia",
        "/Arts & Entertainment/Fun & Trivia/Flash-Based Entertainment",
        "/Arts & Entertainment/Fun & Trivia/Fun Tests & Silly Surveys",
        "/Arts & Entertainment/Humor",
        "/Arts & Entertainment/Humor/Funny Pictures & Videos",
        "/Arts & Entertainment/Humor/Political Humor",
        "/Arts & Entertainment/Movies",
        "/Arts & Entertainment/Music & Audio",
        "/Arts & Entertainment/Music & Audio/CD & Audio Shopping",
        "/Arts & Entertainment/Music & Audio/Classical Music",
        "/Arts & Entertainment/Music & Audio/Country Music",
        "/Arts & Entertainment/Music & Audio/Dance & Electronic Music",
        "/Arts & Entertainment/Music & Audio/Experimental & Industrial Music",
        "/Arts & Entertainment/Music & Audio/Jazz & Blues",
        "/Arts & Entertainment/Music & Audio/Music Education & Instruction",
        "/Arts & Entertainment/Music & Audio/Music Equipment & Technology",
        "/Arts & Entertainment/Music & Audio/Music Reference",
        "/Arts & Entertainment/Music & Audio/Music Streams & Downloads",
        "/Arts & Entertainment/Music & Audio/Music Videos",
        "/Arts & Entertainment/Music & Audio/Pop Music",
        "/Arts & Entertainment/Music & Audio/Radio",
        "/Arts & Entertainment/Music & Audio/Religious Music",
        "/Arts & Entertainment/Music & Audio/Rock Music",
        "/Arts & Entertainment/Music & Audio/Soundtracks",
        "/Arts & Entertainment/Music & Audio/Urban & Hip-Hop",
        "/Arts & Entertainment/Music & Audio/World Music",
        "/Arts & Entertainment/Offbeat",
        "/Arts & Entertainment/Offbeat/Occult & Paranormal",
        "/Arts & Entertainment/Online Media",
        "/Arts & Entertainment/Online Media/Online Image Galleries",
        "/Arts & Entertainment/Performing Arts",
        "/Arts & Entertainment/Performing Arts/Acting & Theater",
        "/Arts & Entertainment/Performing Arts/Circus",
        "/Arts & Entertainment/Performing Arts/Dance",
        "/Arts & Entertainment/Performing Arts/Magic",
        "/Arts & Entertainment/Performing Arts/Opera",
        "/Arts & Entertainment/TV & Video",
        "/Arts & Entertainment/TV & Video/Online Video",
        "/Arts & Entertainment/TV & Video/TV Commercials",
        "/Arts & Entertainment/TV & Video/TV Shows & Programs",
        "/Arts & Entertainment/Visual Art & Design",
        "/Arts & Entertainment/Visual Art & Design/Architecture",
        "/Arts & Entertainment/Visual Art & Design/Art Museums & Galleries",
        "/Arts & Entertainment/Visual Art & Design/Design",
        "/Arts & Entertainment/Visual Art & Design/Painting",
        "/Arts & Entertainment/Visual Art & Design/Photographic & Digital Arts",
        "/Autos & Vehicles",
        "/Autos & Vehicles/Bicycles & Accessories",
        "/Autos & Vehicles/Bicycles & Accessories/Bike Parts & Repair",
        "/Autos & Vehicles/Bicycles & Accessories/BMX Bikes",
        "/Autos & Vehicles/Boats & Watercraft",
        "/Autos & Vehicles/Campers & RVs",
        "/Autos & Vehicles/Classic Vehicles",
        "/Autos & Vehicles/Commercial Vehicles/Cargo Trucks & Trailers",
        "/Autos & Vehicles/Motor Vehicles (By Type)",
        "/Autos & Vehicles/Motor Vehicles (By Type)/Hybrid & Alternative Vehicles",
        "/Autos & Vehicles/Motor Vehicles (By Type)/Motorcycles",
        "/Autos & Vehicles/Motor Vehicles (By Type)/Off-Road Vehicles",
        "/Autos & Vehicles/Motor Vehicles (By Type)/Trucks & SUVs",
        "/Autos & Vehicles/Vehicle Codes & Driving Laws",
        "/Autos & Vehicles/Vehicle Codes & Driving Laws/Vehicle Licensing & Registration",
        "/Autos & Vehicles/Vehicle Parts & Services",
        "/Autos & Vehicles/Vehicle Parts & Services/Gas Prices & Vehicle Fueling",
        "/Autos & Vehicles/Vehicle Parts & Services/Vehicle Parts & Accessories",
        "/Autos & Vehicles/Vehicle Parts & Services/Vehicle Repair & Maintenance",
        "/Autos & Vehicles/Vehicle Shopping",
        "/Autos & Vehicles/Vehicle Shopping/Used Vehicles",
        "/Autos & Vehicles/Vehicle Shows",
        "/Beauty & Fitness",
        "/Beauty & Fitness/Beauty Pageants",
        "/Beauty & Fitness/Body Art",
        "/Beauty & Fitness/Cosmetic Procedures",
        "/Beauty & Fitness/Cosmetic Procedures/Cosmetic Surgery",
        "/Beauty & Fitness/Cosmetology & Beauty Professionals",
        "/Beauty & Fitness/Face & Body Care",
        "/Beauty & Fitness/Face & Body Care/Hygiene & Toiletries",
        "/Beauty & Fitness/Face & Body Care/Make-Up & Cosmetics",
        "/Beauty & Fitness/Face & Body Care/Perfumes & Fragrances",
        "/Beauty & Fitness/Face & Body Care/Skin & Nail Care",
        "/Beauty & Fitness/Face & Body Care/Unwanted Body & Facial Hair Removal",
        "/Beauty & Fitness/Fashion & Style",
        "/Beauty & Fitness/Fashion & Style/Fashion Designers & Collections",
        "/Beauty & Fitness/Fitness",
        "/Beauty & Fitness/Hair Care",
        "/Beauty & Fitness/Hair Care/Hair Loss",
        "/Beauty & Fitness/Spas & Beauty Services",
        "/Beauty & Fitness/Spas & Beauty Services/Massage Therapy",
        "/Beauty & Fitness/Weight Loss",
        "/Books & Literature",
        "/Books & Literature/Children's Literature",
        "/Books & Literature/E-Books",
        "/Books & Literature/Fan Fiction",
        "/Books & Literature/Literary Classics",
        "/Books & Literature/Poetry",
        "/Books & Literature/Writers Resources",
        "/Business & Industrial",
        "/Business & Industrial/Advertising & Marketing/Public Relations",
        "/Business & Industrial/Aerospace & Defense/Space Technology",
        "/Business & Industrial/Agriculture & Forestry",
        "/Business & Industrial/Agriculture & Forestry/Agricultural Equipment",
        "/Business & Industrial/Agriculture & Forestry/Forestry",
        "/Business & Industrial/Agriculture & Forestry/Livestock",
        "/Business & Industrial/Automotive Industry",
        "/Business & Industrial/Business Education",
        "/Business & Industrial/Business Finance",
        "/Business & Industrial/Business Finance/Venture Capital",
        "/Business & Industrial/Business Operations",
        "/Business & Industrial/Business Operations/Business Plans & Presentations",
        "/Business & Industrial/Business Operations/Management",
        "/Business & Industrial/Business Services",
        "/Business & Industrial/Business Services/Consulting",
        "/Business & Industrial/Business Services/Corporate Events",
        "/Business & Industrial/Business Services/E-Commerce Services",
        "/Business & Industrial/Business Services/Fire & Security Services",
        "/Business & Industrial/Business Services/Office Services",
        "/Business & Industrial/Business Services/Office Supplies",
        "/Business & Industrial/Business Services/Writing & Editing Services",
        "/Business & Industrial/Chemicals Industry",
        "/Business & Industrial/Chemicals Industry/Cleaning Agents",
        "/Business & Industrial/Chemicals Industry/Plastics & Polymers",
        "/Business & Industrial/Construction & Maintenance",
        "/Business & Industrial/Construction & Maintenance/Building Materials & Supplies",
        "/Business & Industrial/Energy & Utilities",
        "/Business & Industrial/Energy & Utilities/Electricity",
        "/Business & Industrial/Energy & Utilities/Oil & Gas",
        "/Business & Industrial/Energy & Utilities/Renewable & Alternative Energy",
        "/Business & Industrial/Hospitality Industry",
        "/Business & Industrial/Hospitality Industry/Event Planning",
        "/Business & Industrial/Hospitality Industry/Food Service",
        "/Business & Industrial/Industrial Materials & Equipment",
        "/Business & Industrial/Industrial Materials & Equipment/Heavy Machinery",
        "/Business & Industrial/Manufacturing",
        "/Business & Industrial/Metals & Mining",
        "/Business & Industrial/Metals & Mining/Precious Metals",
        "/Business & Industrial/Pharmaceuticals & Biotech",
        "/Business & Industrial/Printing & Publishing",
        "/Business & Industrial/Retail Trade",
        "/Business & Industrial/Retail Trade/Retail Equipment & Technology",
        "/Business & Industrial/Small Business/MLM & Business Opportunities",
        "/Business & Industrial/Textiles & Nonwovens",
        "/Business & Industrial/Transportation & Logistics",
        "/Business & Industrial/Transportation & Logistics/Freight & Trucking",
        "/Business & Industrial/Transportation & Logistics/Mail & Package Delivery",
        "/Business & Industrial/Transportation & Logistics/Maritime Transport",
        "/Business & Industrial/Transportation & Logistics/Moving & Relocation",
        "/Business & Industrial/Transportation & Logistics/Packaging",
        "/Business & Industrial/Transportation & Logistics/Parking",
        "/Business & Industrial/Transportation & Logistics/Rail Transport",
        "/Business & Industrial/Transportation & Logistics/Urban Transport",
        "/Computers & Electronics",
        "/Computers & Electronics/CAD & CAM",
        "/Computers & Electronics/Computer Hardware",
        "/Computers & Electronics/Computer Hardware/Computer Components",
        "/Computers & Electronics/Computer Hardware/Computer Drives & Storage",
        "/Computers & Electronics/Computer Hardware/Computer Peripherals",
        "/Computers & Electronics/Computer Hardware/Desktop Computers",
        "/Computers & Electronics/Computer Hardware/Laptops & Notebooks",
        "/Computers & Electronics/Computer Security",
        "/Computers & Electronics/Computer Security/Hacking & Cracking",
        "/Computers & Electronics/Consumer Electronics",
        "/Computers & Electronics/Consumer Electronics/Audio Equipment",
        "/Computers & Electronics/Consumer Electronics/Camera & Photo Equipment",
        "/Computers & Electronics/Consumer Electronics/Car Electronics",
        "/Computers & Electronics/Consumer Electronics/Drones & RC Aircraft",
        "/Computers & Electronics/Consumer Electronics/Game Systems & Consoles",
        "/Computers & Electronics/Consumer Electronics/GPS & Navigation",
        "/Computers & Electronics/Consumer Electronics/TV & Video Equipment",
        "/Computers & Electronics/Electronics & Electrical",
        "/Computers & Electronics/Electronics & Electrical/Electronic Components",
        "/Computers & Electronics/Electronics & Electrical/Power Supplies",
        "/Computers & Electronics/Enterprise Technology",
        "/Computers & Electronics/Enterprise Technology/Data Management",
        "/Computers & Electronics/Networking",
        "/Computers & Electronics/Networking/Data Formats & Protocols",
        "/Computers & Electronics/Networking/Network Monitoring & Management",
        "/Computers & Electronics/Networking/VPN & Remote Access",
        "/Computers & Electronics/Programming",
        "/Computers & Electronics/Programming/Java (Programming Language)",
        "/Computers & Electronics/Software",
        "/Computers & Electronics/Software/Business & Productivity Software",
        "/Computers & Electronics/Software/Device Drivers",
        "/Computers & Electronics/Software/Internet Software",
        "/Computers & Electronics/Software/Multimedia Software",
        "/Computers & Electronics/Software/Operating Systems",
        "/Computers & Electronics/Software/Software Utilities",
        "/Finance",
        "/Finance/Accounting & Auditing",
        "/Finance/Accounting & Auditing/Billing & Invoicing",
        "/Finance/Accounting & Auditing/Tax Preparation & Planning",
        "/Finance/Banking",
        "/Finance/Credit & Lending",
        "/Finance/Credit & Lending/Credit Cards",
        "/Finance/Credit & Lending/Credit Reporting & Monitoring",
        "/Finance/Credit & Lending/Loans",
        "/Finance/Financial Planning & Management",
        "/Finance/Financial Planning & Management/Retirement & Pension",
        "/Finance/Grants, Scholarships & Financial Aid",
        "/Finance/Grants, Scholarships & Financial Aid/Study Grants & Scholarships",
        "/Finance/Insurance",
        "/Finance/Insurance/Health Insurance",
        "/Finance/Investing",
        "/Finance/Investing/Commodities & Futures Trading",
        "/Finance/Investing/Currencies & Foreign Exchange",
        "/Finance/Investing/Stocks & Bonds",
        "/Food & Drink",
        "/Food & Drink/Beverages",
        "/Food & Drink/Beverages/Alcoholic Beverages",
        "/Food & Drink/Beverages/Coffee & Tea",
        "/Food & Drink/Beverages/Juice",
        "/Food & Drink/Beverages/Soft Drinks",
        "/Food & Drink/Cooking & Recipes",
        "/Food & Drink/Cooking & Recipes/BBQ & Grilling",
        "/Food & Drink/Cooking & Recipes/Desserts",
        "/Food & Drink/Cooking & Recipes/Soups & Stews",
        "/Food & Drink/Food",
        "/Food & Drink/Food & Grocery Retailers",
        "/Food & Drink/Food/Baked Goods",
        "/Food & Drink/Food/Breakfast Foods",
        "/Food & Drink/Food/Candy & Sweets",
        "/Food & Drink/Food/Grains & Pasta",
        "/Food & Drink/Food/Meat & Seafood",
        "/Food & Drink/Food/Snack Foods",
        "/Food & Drink/Restaurants",
        "/Food & Drink/Restaurants/Fast Food",
        "/Food & Drink/Restaurants/Pizzerias",
        "/Food & Drink/Restaurants/Restaurant Reviews & Reservations",
        "/Games",
        "/Games/Arcade & Coin-Op Games",
        "/Games/Board Games",
        "/Games/Board Games/Chess & Abstract Strategy Games",
        "/Games/Board Games/Miniatures & Wargaming",
        "/Games/Card Games",
        "/Games/Card Games/Collectible Card Games",
        "/Games/Card Games/Poker & Casino Games",
        "/Games/Computer & Video Games",
        "/Games/Computer & Video Games/Casual Games",
        "/Games/Computer & Video Games/Driving & Racing Games",
        "/Games/Computer & Video Games/Fighting Games",
        "/Games/Computer & Video Games/Music & Dance Games",
        "/Games/Computer & Video Games/Sandbox Games",
        "/Games/Computer & Video Games/Shooter Games",
        "/Games/Computer & Video Games/Simulation Games",
        "/Games/Computer & Video Games/Sports Games",
        "/Games/Computer & Video Games/Strategy Games",
        "/Games/Computer & Video Games/Video Game Emulation",
        "/Games/Family-Oriented Games & Activities",
        "/Games/Family-Oriented Games & Activities/Drawing & Coloring",
        "/Games/Family-Oriented Games & Activities/Dress-Up & Fashion Games",
        "/Games/Gambling",
        "/Games/Gambling/Lottery",
        "/Games/Online Games/Massively Multiplayer Games",
        "/Games/Puzzles & Brainteasers",
        "/Games/Roleplaying Games",
        "/Games/Table Games",
        "/Games/Table Games/Billiards",
        "/Games/Word Games",
        "/Health",
        "/Health/Aging & Geriatrics",
        "/Health/Health Conditions",
        "/Health/Health Conditions/AIDS & HIV",
        "/Health/Health Conditions/Allergies",
        "/Health/Health Conditions/Arthritis",
        "/Health/Health Conditions/Cancer",
        "/Health/Health Conditions/Diabetes",
        "/Health/Health Conditions/Ear Nose & Throat",
        "/Health/Health Conditions/Eating Disorders",
        "/Health/Health Conditions/Endocrine Conditions",
        "/Health/Health Conditions/Genetic Disorders",
        "/Health/Health Conditions/Heart & Hypertension",
        "/Health/Health Conditions/Infectious Diseases",
        "/Health/Health Conditions/Neurological Conditions",
        "/Health/Health Conditions/Obesity",
        "/Health/Health Conditions/Pain Management",
        "/Health/Health Conditions/Respiratory Conditions",
        "/Health/Health Conditions/Skin Conditions",
        "/Health/Health Conditions/Sleep Disorders",
        "/Health/Health Education & Medical Training",
        "/Health/Health Foundations & Medical Research",
        "/Health/Medical Devices & Equipment",
        "/Health/Medical Facilities & Services",
        "/Health/Medical Facilities & Services/Doctors' Offices",
        "/Health/Medical Facilities & Services/Hospitals & Treatment Centers",
        "/Health/Medical Facilities & Services/Medical Procedures",
        "/Health/Medical Facilities & Services/Physical Therapy",
        "/Health/Men's Health",
        "/Health/Mental Health",
        "/Health/Mental Health/Anxiety & Stress",
        "/Health/Mental Health/Depression",
        "/Health/Nursing",
        "/Health/Nursing/Assisted Living & Long Term Care",
        "/Health/Nutrition",
        "/Health/Nutrition/Special & Restricted Diets",
        "/Health/Nutrition/Vitamins & Supplements",
        "/Health/Oral & Dental Care",
        "/Health/Pharmacy",
        "/Health/Pharmacy/Drugs & Medications",
        "/Health/Public Health",
        "/Health/Public Health/Occupational Health & Safety",
        "/Health/Reproductive Health",
        "/Health/Substance Abuse",
        "/Health/Substance Abuse/Drug & Alcohol Testing",
        "/Health/Substance Abuse/Drug & Alcohol Treatment",
        "/Health/Substance Abuse/Smoking & Smoking Cessation",
        "/Health/Substance Abuse/Steroids & Performance-Enhancing Drugs",
        "/Health/Vision Care",
        "/Health/Vision Care/Eyeglasses & Contacts",
        "/Health/Women's Health",
        "/Hobbies & Leisure",
        "/Hobbies & Leisure/Clubs & Organizations",
        "/Hobbies & Leisure/Clubs & Organizations/Youth Organizations & Resources",
        "/Hobbies & Leisure/Crafts",
        "/Hobbies & Leisure/Crafts/Fiber & Textile Arts",
        "/Hobbies & Leisure/Merit Prizes & Contests",
        "/Hobbies & Leisure/Outdoors",
        "/Hobbies & Leisure/Outdoors/Fishing",
        "/Hobbies & Leisure/Outdoors/Hiking & Camping",
        "/Hobbies & Leisure/Paintball",
        "/Hobbies & Leisure/Radio Control & Modeling",
        "/Hobbies & Leisure/Radio Control & Modeling/Model Trains & Railroads",
        "/Hobbies & Leisure/Special Occasions",
        "/Hobbies & Leisure/Special Occasions/Holidays & Seasonal Events",
        "/Hobbies & Leisure/Special Occasions/Weddings",
        "/Hobbies & Leisure/Water Activities",
        "/Hobbies & Leisure/Water Activities/Boating",
        "/Hobbies & Leisure/Water Activities/Surf & Swim",
        "/Home & Garden",
        "/Home & Garden/Bed & Bath",
        "/Home & Garden/Bed & Bath/Bathroom",
        "/Home & Garden/Domestic Services",
        "/Home & Garden/Domestic Services/Cleaning Services",
        "/Home & Garden/Gardening & Landscaping",
        "/Home & Garden/Home & Interior Decor",
        "/Home & Garden/Home Appliances",
        "/Home & Garden/Home Furnishings",
        "/Home & Garden/Home Furnishings/Curtains & Window Treatments",
        "/Home & Garden/Home Furnishings/Kitchen & Dining Furniture",
        "/Home & Garden/Home Furnishings/Lamps & Lighting",
        "/Home & Garden/Home Furnishings/Living Room Furniture",
        "/Home & Garden/Home Furnishings/Rugs & Carpets",
        "/Home & Garden/Home Improvement",
        "/Home & Garden/Home Improvement/Construction & Power Tools",
        "/Home & Garden/Home Improvement/Doors & Windows",
        "/Home & Garden/Home Improvement/Flooring",
        "/Home & Garden/Home Improvement/House Painting & Finishing",
        "/Home & Garden/Home Improvement/Plumbing",
        "/Home & Garden/Home Safety & Security",
        "/Home & Garden/Home Storage & Shelving",
        "/Home & Garden/Home Swimming Pools, Saunas & Spas",
        "/Home & Garden/HVAC & Climate Control",
        "/Home & Garden/HVAC & Climate Control/Fireplaces & Stoves",
        "/Home & Garden/Kitchen & Dining",
        "/Home & Garden/Kitchen & Dining/Cookware & Diningware",
        "/Home & Garden/Kitchen & Dining/Major Kitchen Appliances",
        "/Home & Garden/Kitchen & Dining/Small Kitchen Appliances",
        "/Home & Garden/Laundry",
        "/Home & Garden/Laundry/Washers & Dryers",
        "/Home & Garden/Nursery & Playroom",
        "/Home & Garden/Pest Control",
        "/Home & Garden/Yard & Patio",
        "/Home & Garden/Yard & Patio/Lawn Mowers",
        "/Internet & Telecom",
        "/Internet & Telecom/Communications Equipment",
        "/Internet & Telecom/Communications Equipment/Radio Equipment",
        "/Internet & Telecom/Email & Messaging",
        "/Internet & Telecom/Email & Messaging/Text & Instant Messaging",
        "/Internet & Telecom/Email & Messaging/Voice & Video Chat",
        "/Internet & Telecom/Mobile & Wireless",
        "/Internet & Telecom/Mobile & Wireless/Mobile & Wireless Accessories",
        "/Internet & Telecom/Mobile & Wireless/Mobile Apps & Add-Ons",
        "/Internet & Telecom/Mobile & Wireless/Mobile Phones",
        "/Internet & Telecom/Service Providers",
        "/Internet & Telecom/Service Providers/Cable & Satellite Providers",
        "/Internet & Telecom/Web Services",
        "/Internet & Telecom/Web Services/Affiliate Programs",
        "/Internet & Telecom/Web Services/Web Design & Development",
        "/Jobs & Education",
        "/Jobs & Education/Education",
        "/Jobs & Education/Education/Colleges & Universities",
        "/Jobs & Education/Education/Distance Learning",
        "/Jobs & Education/Education/Homeschooling",
        "/Jobs & Education/Education/Primary & Secondary Schooling (K-12)",
        "/Jobs & Education/Education/Standardized & Admissions Tests",
        "/Jobs & Education/Education/Teaching & Classroom Resources",
        "/Jobs & Education/Education/Training & Certification",
        "/Jobs & Education/Education/Vocational & Continuing Education",
        "/Jobs & Education/Jobs",
        "/Jobs & Education/Jobs/Career Resources & Planning",
        "/Jobs & Education/Jobs/Job Listings",
        "/Jobs & Education/Jobs/Resumes & Portfolios",
        "/Law & Government",
        "/Law & Government/Government",
        "/Law & Government/Government/Courts & Judiciary",
        "/Law & Government/Government/Visa & Immigration",
        "/Law & Government/Legal",
        "/Law & Government/Legal/Bankruptcy",
        "/Law & Government/Legal/Legal Education",
        "/Law & Government/Legal/Legal Services",
        "/Law & Government/Military",
        "/Law & Government/Public Safety",
        "/Law & Government/Public Safety/Crime & Justice",
        "/Law & Government/Public Safety/Emergency Services",
        "/Law & Government/Public Safety/Law Enforcement",
        "/Law & Government/Public Safety/Security Products & Services",
        "/Law & Government/Social Services",
        "/News",
        "/News/Business News",
        "/News/Business News/Company News",
        "/News/Business News/Financial Markets News",
        "/News/Gossip & Tabloid News/Scandals & Investigations",
        "/News/Health News",
        "/News/Politics",
        "/News/Sports News",
        "/News/Weather",
        "/Online Communities",
        "/Online Communities/Blogging Resources & Services",
        "/Online Communities/Dating & Personals",
        "/Online Communities/Dating & Personals/Matrimonial Services",
        "/Online Communities/Dating & Personals/Personals",
        "/Online Communities/Dating & Personals/Photo Rating Sites",
        "/Online Communities/File Sharing & Hosting",
        "/Online Communities/Online Goodies",
        "/Online Communities/Online Goodies/Clip Art & Animated GIFs",
        "/Online Communities/Online Goodies/Skins, Themes & Wallpapers",
        "/Online Communities/Online Goodies/Social Network Apps & Add-Ons",
        "/Online Communities/Photo & Video Sharing",
        "/Online Communities/Photo & Video Sharing/Photo & Image Sharing",
        "/Online Communities/Social Networks",
        "/Online Communities/Virtual Worlds",
        "/People & Society",
        "/People & Society/Family & Relationships",
        "/People & Society/Family & Relationships/Family",
        "/People & Society/Family & Relationships/Marriage",
        "/People & Society/Family & Relationships/Troubled Relationships",
        "/People & Society/Kids & Teens",
        "/People & Society/Kids & Teens/Children's Interests",
        "/People & Society/Kids & Teens/Teen Interests",
        "/People & Society/Religion & Belief",
        "/People & Society/Seniors & Retirement",
        "/People & Society/Social Issues & Advocacy",
        "/People & Society/Social Issues & Advocacy/Charity & Philanthropy",
        "/People & Society/Social Issues & Advocacy/Discrimination & Identity Relations",
        "/People & Society/Social Issues & Advocacy/Green Living & Environmental Issues",
        "/People & Society/Social Issues & Advocacy/Human Rights & Liberties",
        "/People & Society/Social Issues & Advocacy/Poverty & Hunger",
        "/People & Society/Social Issues & Advocacy/Work & Labor Issues",
        "/People & Society/Social Sciences",
        "/People & Society/Social Sciences/Economics",
        "/People & Society/Social Sciences/Political Science",
        "/People & Society/Social Sciences/Psychology",
        "/People & Society/Subcultures & Niche Interests",
        "/Pets & Animals",
        "/Pets & Animals/Animal Products & Services/Pet Food & Supplies",
        "/Pets & Animals/Animal Products & Services/Veterinarians",
        "/Pets & Animals/Pets",
        "/Pets & Animals/Pets/Birds",
        "/Pets & Animals/Pets/Cats",
        "/Pets & Animals/Pets/Dogs",
        "/Pets & Animals/Pets/Exotic Pets",
        "/Pets & Animals/Pets/Fish & Aquaria",
        "/Pets & Animals/Pets/Horses",
        "/Pets & Animals/Pets/Rabbits & Rodents",
        "/Pets & Animals/Pets/Reptiles & Amphibians",
        "/Pets & Animals/Wildlife",
        "/Real Estate",
        "/Real Estate/Real Estate Listings",
        "/Real Estate/Real Estate Listings/Bank-Owned & Foreclosed Properties",
        "/Real Estate/Real Estate Listings/Commercial Properties",
        "/Real Estate/Real Estate Listings/Lots & Land",
        "/Real Estate/Real Estate Listings/Residential Rentals",
        "/Real Estate/Real Estate Listings/Residential Sales",
        "/Real Estate/Real Estate Listings/Timeshares & Vacation Properties",
        "/Real Estate/Real Estate Services",
        "/Reference",
        "/Reference/Directories & Listings",
        "/Reference/Directories & Listings/Business & Personal Listings",
        "/Reference/General Reference",
        "/Reference/General Reference/Biographies & Quotations",
        "/Reference/General Reference/Calculators & Reference Tools",
        "/Reference/General Reference/Dictionaries & Encyclopedias",
        "/Reference/General Reference/Forms Guides & Templates",
        "/Reference/General Reference/Public Records",
        "/Reference/General Reference/Time & Calendars",
        "/Reference/Geographic Reference",
        "/Reference/Geographic Reference/Maps",
        "/Reference/Humanities",
        "/Reference/Humanities/History",
        "/Reference/Humanities/Myth & Folklore",
        "/Reference/Humanities/Philosophy",
        "/Reference/Language Resources",
        "/Reference/Language Resources/Foreign Language Resources",
        "/Reference/Libraries & Museums",
        "/Reference/Libraries & Museums/Museums",
        "/Science",
        "/Science/Astronomy",
        "/Science/Biological Sciences",
        "/Science/Biological Sciences/Neuroscience",
        "/Science/Chemistry",
        "/Science/Computer Science",
        "/Science/Earth Sciences",
        "/Science/Earth Sciences/Atmospheric Science",
        "/Science/Earth Sciences/Geology",
        "/Science/Ecology & Environment",
        "/Science/Ecology & Environment/Climate Change & Global Warming",
        "/Science/Engineering & Technology",
        "/Science/Engineering & Technology/Robotics",
        "/Science/Mathematics",
        "/Science/Mathematics/Statistics",
        "/Science/Physics",
        "/Science/Scientific Institutions",
        "/Sensitive Subjects",
        "/Shopping",
        "/Shopping/Antiques & Collectibles",
        "/Shopping/Apparel",
        "/Shopping/Apparel/Athletic Apparel",
        "/Shopping/Apparel/Casual Apparel",
        "/Shopping/Apparel/Children's Clothing",
        "/Shopping/Apparel/Clothing Accessories",
        "/Shopping/Apparel/Costumes",
        "/Shopping/Apparel/Eyewear",
        "/Shopping/Apparel/Footwear",
        "/Shopping/Apparel/Formal Wear",
        "/Shopping/Apparel/Headwear",
        "/Shopping/Apparel/Men's Clothing",
        "/Shopping/Apparel/Swimwear",
        "/Shopping/Apparel/Undergarments",
        "/Shopping/Apparel/Women's Clothing",
        "/Shopping/Auctions",
        "/Shopping/Classifieds",
        "/Shopping/Consumer Resources",
        "/Shopping/Consumer Resources/Consumer Advocacy & Protection",
        "/Shopping/Consumer Resources/Coupons & Discount Offers",
        "/Shopping/Consumer Resources/Product Reviews & Price Comparisons",
        "/Shopping/Entertainment Media",
        "/Shopping/Entertainment Media/Entertainment Media Rentals",
        "/Shopping/Gifts & Special Event Items",
        "/Shopping/Gifts & Special Event Items/Cards & Greetings",
        "/Shopping/Gifts & Special Event Items/Flowers",
        "/Shopping/Gifts & Special Event Items/Gifts",
        "/Shopping/Luxury Goods",
        "/Shopping/Mass Merchants & Department Stores",
        "/Shopping/Photo & Video Services",
        "/Shopping/Tobacco Products",
        "/Shopping/Toys",
        "/Shopping/Toys/Building Toys",
        "/Shopping/Toys/Die-cast & Toy Vehicles",
        "/Shopping/Toys/Dolls & Accessories",
        "/Shopping/Toys/Ride-On Toys & Wagons",
        "/Shopping/Toys/Stuffed Toys",
        "/Sports",
        "/Sports/Animal Sports",
        "/Sports/College Sports",
        "/Sports/Combat Sports",
        "/Sports/Combat Sports/Boxing",
        "/Sports/Combat Sports/Martial Arts",
        "/Sports/Combat Sports/Wrestling",
        "/Sports/Extreme Sports",
        "/Sports/Extreme Sports/Drag & Street Racing",
        "/Sports/Fantasy Sports",
        "/Sports/Individual Sports",
        "/Sports/Individual Sports/Cycling",
        "/Sports/Individual Sports/Golf",
        "/Sports/Individual Sports/Gymnastics",
        "/Sports/Individual Sports/Racquet Sports",
        "/Sports/Individual Sports/Skate Sports",
        "/Sports/Individual Sports/Track & Field",
        "/Sports/International Sports Competitions",
        "/Sports/International Sports Competitions/Olympics",
        "/Sports/Motor Sports",
        "/Sports/Sporting Goods",
        "/Sports/Sporting Goods/Sports Memorabilia",
        "/Sports/Sporting Goods/Winter Sports Equipment",
        "/Sports/Sports Coaching & Training",
        "/Sports/Team Sports",
        "/Sports/Team Sports/American Football",
        "/Sports/Team Sports/Australian Football",
        "/Sports/Team Sports/Baseball",
        "/Sports/Team Sports/Basketball",
        "/Sports/Team Sports/Cheerleading",
        "/Sports/Team Sports/Cricket",
        "/Sports/Team Sports/Hockey",
        "/Sports/Team Sports/Rugby",
        "/Sports/Team Sports/Soccer",
        "/Sports/Team Sports/Volleyball",
        "/Sports/Water Sports",
        "/Sports/Water Sports/Surfing",
        "/Sports/Water Sports/Swimming",
        "/Sports/Winter Sports",
        "/Sports/Winter Sports/Ice Skating",
        "/Sports/Winter Sports/Skiing & Snowboarding",
        "/Travel",
        "/Travel/Air Travel",
        "/Travel/Air Travel/Airport Parking & Transportation",
        "/Travel/Bus & Rail",
        "/Travel/Car Rental & Taxi Services",
        "/Travel/Cruises & Charters",
        "/Travel/Hotels & Accommodations",
        "/Travel/Hotels & Accommodations/Vacation Rentals & Short-Term Stays",
        "/Travel/Specialty Travel",
        "/Travel/Tourist Destinations",
        "/Travel/Tourist Destinations/Beaches & Islands",
        "/Travel/Tourist Destinations/Mountain & Ski Resorts",
        "/Travel/Tourist Destinations/Regional Parks & Gardens",
        "/Travel/Tourist Destinations/Theme Parks",
        "/Travel/Tourist Destinations/Zoos-Aquariums-Preserves"
    ]
    subtag_arr = []
    for category in category_arr:
        category = category.split("/")
        subtag_arr.append(category[-1])
    return subtag_arr

def main():
    pdf_path = "cat.pdf"
    png_path = "fnce100.png"
    # generate_tags_pdf(pdf_path)
    # generate_tags_image(png_path)
    # generate_images(pdf_path)

if __name__ == "__main__":
    main()

# def generate_images(pdf_path):
#     file = pdf_path
#     pdf_file = fitz.open(file)
#     for page_index in range(6):
#         # get the page itself
#         page = pdf_file[page_index]
#         image_list = page.getImageList()
#         # printing number of images found in this page
#         if image_list:
#             print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
#         else:
#             print("[!] No images found on page", page_index)
#         for image_index, img in enumerate(page.getImageList(), start=1):
#             # get the XREF of the image
#             xref = img[0]
#             # extract the image bytes
#             base_image = pdf_file.extractImage(xref)
#             image_bytes = base_image["image"]
#             # get the image extension
#             image_ext = base_image["ext"]
#             # load it to PIL
#             image = Image.open(io.BytesIO(image_bytes))
#             # save it to local disk
#             image.save(open(f"image{page_index+1}_{image_index}.{image_ext}", "wb"))