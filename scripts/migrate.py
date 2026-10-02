#!/usr/bin/env python3
"""Migrate the Sidestage inventory into src/events/*.md files."""
import os
import re
import unicodedata
from datetime import datetime

SITE = os.path.expanduser("~/workspace/sidestage-website/site")
EVDIR = os.path.join(SITE, "src", "events")
IMGDIR = os.path.join(SITE, "src", "img", "events")


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-+", "-", s)


def yq(s):
    """YAML-quote a scalar string."""
    s = str(s)
    if s == "":
        return '""'
    if re.search(r'[:#\[\]{},&*!|>\'"%@`]|^\s|\s$', s) or "\n" in s:
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


# (artist, title, date, venue, city, ticket_link, flyer_basename_or_empty, sold_out)
EVENTS_2025 = [
    ("Sematary", "", "2025-07-29", "The Mod Club", "Toronto", "",
     "Static_Social_Facebook_1920x1080_Sematary_2025_Regional_TheModClub_0729.jpg", False),
    ("DJ Lex", "", "2025-08-22", "The Mod Club", "Toronto", "",
     "1920x1080_DJ-LEX_Toronto.jpg", False),
    ("Giggs", "", "2025-09-04", "Theatre Fairmount", "Montreal", "",
     "BANNER_Giggs.png", False),
    ("Giggs", "", "2025-09-05", "The Mod Club", "Toronto", "",
     "Giggs_1920x1080.jpg", False),
    ("Mild Orange", "", "2025-09-24", "Longboat Hall", "Toronto", "",
     "Static_Social_Facebook_1920x1080_MildOrange_2025_Regional_LongboatHall_0924_BOYO.jpg", False),
    ("Lil Tracy", "", "2025-09-29", "The Concert Hall", "Toronto", "",
     "Static_Social_Facebook_1920x1080_LilTracy_2025_Regional_TheConcertHall_0929.jpg", False),
    ("Cash Cobain", "", "2025-10-05", "Phoenix Concert Theatre", "Toronto", "",
     "Static_Social_Facebook_1920x1080_CashCobain_2025_Regional_PhoenixConcertTheatre_1005_SidestagePresents.jpg", False),
    ("Cash Cobain", "", "2025-10-07", "Club Soda", "Montreal", "",
     "Cash-Cobain---MTL-horizontal.jpg", False),
    ("Bladee", "", "2025-10-12", "History", "Toronto", "",
     "Bladee_2025_1920x1080.jpg", False),
    ("James Vickery", "", "2025-10-30", "Velvet Underground", "Toronto", "",
     "Static_Social_Facebook_1920x1005_JamesVickery_2025_Regional_VelvetUnderground_1030.jpg", False),
]

EVENTS_2022_2023 = [
    ("IDK", "", "2023-10-29", "Adelaide Hall", "Toronto",
     "https://admitone.com/events/idk-toronto-8878721", "IDK_HEADER.jpg", False),
    ("Little Simz", "", "2023-10-08", "HISTORY", "Toronto",
     "https://www.ticketmaster.ca/event/10005E85EF993CB2", "LittleSimz_Header.jpg", False),
    ("KAMAUU", "", "2023-09-15", "Drake Underground", "Toronto",
     "https://www.ticketweb.ca/event/kamauu-drake-underground-tickets/13209648?pl=embrace", "", False),
    ("nothing,nowhere.", "", "2023-09-13", "Phoenix Concert Theatre", "Toronto",
     "https://www.ticketweb.ca/event/nothingnowhere-seeyouspacecowboy-static-dress-moodring-the-phoenix-concert-theatre-tickets/13270448?pl=embrace",
     "ve_portrait_blank.jpg", False),
    ("Boldy James", "", "2023-07-07", "Velvet Underground", "Toronto",
     "https://www.ticketweb.ca/event/boldy-james-guests-velvet-underground-tickets/13268278?pl=embrace",
     "BoldyJames_Header.jpg", False),
    ("ZelooperZ", "", "2023-06-25", "The Garrison", "Toronto",
     "https://www.ticketweb.ca/event/zelooperz-the-garrison-tickets/13201488?pl=embrace",
     "ZelooperZ_Header.jpg", False),
    ("KayCyy", "", "2023-06-23", "Velvet Underground", "Toronto",
     "https://www.ticketweb.ca/event/kaycyy-velvet-underground-tickets/13223248?pl=embrace",
     "Static_Social-Twitter_800x419_KayCyy_2023_Regional_TheAxisClub_0623.jpg", False),
    ("Various Artists", "Sundown Solstice Festival", "2023-06-16", "Cuddy Park", "Anchorage",
     "https://www.sundownalaska.com/", "Announce-Poster-Horizontal.jpg", False),
    ("Various Artists", "MURAL Festival", "2023-06-09", "Parc Olympique", "Montreal",
     "https://festivalmural.laissezpasser.net/fr/liste/programmation/",
     "Snapinsta.app_343913067_543339977978503_5130356259108965164_n.jpg", False),
    ("James Vickery", "", "2023-05-21", "Drake Underground", "Toronto",
     "https://www.facebook.com/events/594009138789700", "JAMESVICKERY_HEADER.jpg", False),
    ("Joony", "", "2023-05-07", "Drake Underground", "Toronto",
     "https://www.ticketweb.ca/event/joony-drake-underground-tickets/13113765?pl=embrace",
     "Joony_Header.jpg", False),
    ("Aitch", "", "2023-04-11", "Theatre Fairmount", "Montreal",
     "https://www.universe.com/events/aitch-tickets-8WJ7TZ", "1.jpg", False),
    ("Freddie Gibbs", "", "2023-04-08", "The Palace Theatre", "Calgary",
     "https://www.ticketweb.ca/event/freddie-gibbs-calgary-the-palace-theatre-tickets/12882435?pl=TwoTowers",
     "Freddie-Gibbs-Ticketweb-(16x9).jpg", False),
    ("Freddie Gibbs", "", "2023-04-07", "Union Hall", "Edmonton",
     "https://www.ticketweb.ca/event/freddie-gibbs-union-hall-tickets/12881355?pl=UnionHall",
     "GIBBS-16x9.png", False),
    ("RINI", "", "2023-04-06", "TD Music Hall", "Toronto",
     "https://www.facebook.com/events/1914245558922391", "RINI_Header.jpg", False),
    ("Freddie Dredd", "", "2023-03-18", "Velvet Underground", "Toronto",
     "https://www.ticketweb.ca/event/freddie-dredd-velvet-underground-tickets/12814765?pl=embrace",
     "Press-Photo.jpg", False),
    ("\u00bfT\u00e9o?", "", "2023-03-15", "Velvet Underground", "Toronto",
     "https://www.ticketweb.ca/event/-to-the-velvet-underground-tickets/12603185?pl=embrace",
     "Teo_Header.jpg", False),
    ("Anna of The North", "", "2023-03-24", "Velvet Underground", "Toronto",
     "https://www.ticketweb.ca/event/anna-of-the-north-the-velvet-underground-tickets/12613475?pl=embrace",
     "IMG_0439.jpg", False),
    ("Lil Tjay", "", "2023-03-08", "EY Centre", "Ottawa",
     "https://www.eventbrite.ca/e/lil-tjay-killy-live-in-ottawa-march-8th-tickets-515354768987",
     "Facebook-Event.jpg", False),
    ("Lil Tjay", "", "2023-03-05", "Burton Cummings Theatre", "Winnipeg",
     "https://www.ticketmaster.ca/event/11005E306DC81056", "Facebook-Event.jpg", False),
    ("Lil Tjay", "", "2023-03-03", "Union Hall", "Edmonton",
     "https://www.ticketweb.ca/event/lil-tjay-union-hall-tickets/12836575?pl=UnionHall",
     "Facebook-Event.jpg", False),
    ("Lil Tjay", "", "2023-03-02", "Grey Eagle Event Centre", "Calgary",
     "https://www.ticketmaster.ca/event/11005E300C003726", "Facebook-Event.jpg", False),
    ("Sematary", "", "2023-02-24", "Velvet Underground", "Toronto",
     "https://www.ticketweb.ca/event/sematary-velvet-underground-tickets/12633915?pl=embrace",
     "Sematary_Header.jpg", True),
    ("Sematary", "2nd Show", "2023-02-23", "Velvet Underground", "Toronto",
     "https://www.ticketweb.ca/event/sematary-velvet-underground-tickets/12633915?pl=embrace",
     "Sematary_Header.jpg", False),
    ("Riz La Vie", "", "2023-02-22", "Newspeak", "Montreal", "",
     "RizLaVie_Admat_FB.png", False),
    ("Inayah", "", "2023-02-17", "Drake Underground", "Toronto",
     "https://www.ticketweb.ca/event/inayah-drake-underground-tickets/12827355",
     "323949321_499805715385586_3523075867674736673_n.jpg", False),
    ("SXMPRA & LILBUBBLEGUM", "", "2023-02-16", "Velvet Underground", "Toronto",
     "https://www.ticketweb.ca/event/sxmpra-lilbubblegum-velvet-underground-tickets/12736355?pl=embrace",
     "SXMPRAandlilbubblegum_HEADER.jpg", False),
    ("Nemahsis", "", "2023-02-16", "The Great Hall", "Toronto",
     "https://www.ticketweb.ca/event/nemahsis-the-great-hall-tickets/12727405?pl=embrace",
     "IMG_0649.jpg", False),
    ("Abhi the Nomad", "", "2022-11-19", "Drake Underground", "Toronto",
     "https://www.ticketweb.ca/event/abhi-the-nomad-charlie-curtis-drake-underground-tickets/12361735",
     "IMG_9835.jpg", False),
    ("RealestK", "", "2022-11-10", "The Axis Club", "Toronto",
     "https://www.ticketweb.ca/event/realestk-the-axis-club-tickets/12533685?pl=embrace",
     "RealestK_Header.jpg", False),
    ("Montell Fish", "", "2022-11-06", "Longboat Hall", "Toronto",
     "https://www.ticketweb.ca/event/montell-fish-longboat-hall-tickets/12418885?pl=embrace",
     "MontellFish_Header.jpg", False),
    ("Tommy Cash", "", "2022-11-02", "The Opera House", "Toronto",
     "https://www.ticketweb.ca/event/tommy-cash-the-opera-house-tickets/12412925",
     "IMG_9911.jpg", False),
    ("Tommy Cash", "", "2022-11-01", "Theatre Fairmount", "Montreal",
     "https://www.iloveneon.ca/", "IMG_9913.jpg", False),
    ("Kenyon Dixon", "", "2022-11-01", "Drake Underground", "Toronto",
     "https://www.ticketweb.ca/event/kenyon-dixon-drake-underground-tickets/12509505?pl=embrace",
     "KenyonDixon_Header.jpg", False),
    ("Joey Pecoraro", "", "2022-10-22", "Velvet Underground", "Toronto",
     "https://www.ticketweb.ca/event/joey-pecoraro-the-velvet-underground-tickets/12093605?pl=embrace",
     "JoeyPecoraro_Header.jpg", False),
    ("CKay", "", "2022-10-18", "Studio TD", "Montreal",
     "https://www.ticketmaster.ca/event/31005D13D79A577F?brand=evenko&lang=en-ca",
     "CKay_Admat_FB.png", False),
    ("DUCKWRTH", "", "2022-10-07", "Bar Le Ritz PDB", "Montreal",
     "https://www.ticketmaster.ca/event/31005CB2EBE83F59", "Duckwrth_Admat_FB.png", False),
    ("DUCKWRTH", "", "2022-10-06", "The Axis Club", "Toronto",
     "https://www.ticketweb.ca/event/duckwrth-the-axis-club-tickets/12132585?pl=embrace",
     "Duckwrth_Header.jpg", False),
    ("Rexx Life Raj", "", "2022-10-03", "Velvet Underground", "Toronto",
     "https://www.facebook.com/events/1003127550376607", "IMG_9700.jpg", False),
    ("Freddie Gibbs & Zack Fox", "", "2022-06-03", "Commodore Ballroom", "Vancouver",
     "https://www.ticketmaster.ca/event/11005B8ED4973781", "fb2.png", False),
]

EVENTS_2020_2022 = [
    ("nothing,nowhere.", "", "2022-05-24", "The Opera House", "Toronto", "",
     "NothingNowhere_Header.jpg", False),
    ("Turnstile", "", "2022-05-19", "Phoenix Concert Theatre", "Toronto",
     "https://www.ticketweb.ca/event/turnstile-citizen-truth-cult-the-phoenix-concert-theatre-tickets/11529995?pl=embrace",
     "Turnstile_Header.jpg", False),
    ("Little Simz", "", "2022-05-17", "Phoenix Concert Theatre", "Toronto",
     "https://www.ticketweb.ca/event/little-simz-the-phoenix-concert-theatre-tickets/11360005?pl=embrace",
     "243687132_5176401752388668_1781426989681064440_n.jpg", False),
    ("Mariah The Scientist", "", "2022-05-08", "The Opera House", "Toronto",
     "https://www.ticketweb.ca/event/mariah-the-scientist-the-opera-house-tickets/11885805?pl=embrace",
     "MariahTheScientist_Header.jpg", False),
    ("Conway the Machine", "", "2022-05-08", "Le National", "Montreal",
     "https://latribu-lenational.tuxedobillet.com/Le%20National/conway-the-machine",
     "1064D157-5985-4C0B-88DF-1BBCF257B86B.png", False),
    ("Conway the Machine", "", "2022-05-07", "Danforth Music Hall", "Toronto",
     "https://www.ticketmaster.ca/event/10005B89CA94285A",
     "9388D94A-3459-4AE7-A29C-B70B3E7CD783.png", False),
    ("Conway the Machine", "", "2022-05-06", "London Music Hall", "London",
     "https://www.ticketweb.ca/event/conway-the-machine-london-music-hall-tickets/11610305",
     "F83CE670-D33D-4DE1-9FB5-C42F1AA1CEA0.png", False),
    ("Conway the Machine", "", "2022-05-04", "Marquee Ballroom", "Halifax",
     "https://www.showpass.com/conway-the-machine-x-national-tour-halifax/",
     "LGGYK_CANADA.png", False),
    ("Conway the Machine", "", "2022-05-03", "Exchange Event Centre", "Winnipeg",
     "https://www.ticketweb.ca/event/conway-the-machine-beanz-exchange-event-centre-tickets/11610145",
     "996BDDEB-5288-4202-A3B3-8C5E2ECE8DEA.png", False),
    ("Conway the Machine", "", "2022-04-30", "Union Hall", "Edmonton",
     "https://www.ticketweb.ca/event/conway-the-machine-beanz-union-hall-tickets/11610255",
     "36A0C13B-DA7F-4C25-9CD1-4173ED2885CC.png", False),
    ("Conway the Machine", "", "2022-04-29", "Commonwealth Bar & Stage", "Calgary",
     "https://www.ticketweb.ca/event/conway-the-machine-commonwealth-bar-stage-tickets/11614985",
     "50FE9AB5-159D-4AC5-A29C-E30BB2E84A73.png", False),
    ("Conway the Machine", "", "2022-04-27", "Fortune Sound Club", "Vancouver",
     "https://www.ticketweb.ca/event/conway-the-machine-fortune-sound-club-tickets/11615065?pl=blueprint",
     "CB92612F-6F38-42B0-9126-8D60D0FFC2CC.png", False),
    ("Conway the Machine", "", "2022-04-26", "Upstairs Cabaret", "Victoria",
     "https://www.eventbrite.ca/e/conway-the-machine-tickets-224888717207",
     "LGGYK_CANADA.png", False),
    ("Killy", "", "2022-04-24", "The Axis Club", "Toronto",
     "https://www.ticketweb.ca/event/killy-the-axis-club-formerly-the-tickets/11357245?pl=embrace",
     "Killy_Header.jpg", False),
    ("Eryn Martin", "", "2022-03-19", "Drake Underground", "Toronto",
     "https://www.ticketweb.ca/event/eryn-martin-drake-underground-tickets/11575405?pl=embrace",
     "ErynMartin_Header.jpg", False),
    ("Tommy Cash", "", "2022-03-04", "Le National", "Montreal",
     "https://latribu-lenational.tuxedobillet.com/Le%20National/tommy%20cash",
     "Tommy-Cash---Approved-Photo-1.jpg", False),
    ("Tommy Cash", "", "2022-03-02", "Velvet Underground", "Toronto",
     "https://www.ticketweb.ca/event/tommy-cash-the-velvet-underground-tickets/10983235?pl=embrace",
     "Tommy-Cash---Approved-Photo-1.jpg", False),
    ("Action Bronson & Earl Sweatshirt", "", "2022-02-14", "History", "Toronto",
     "https://www.ticketmaster.ca/event/10005B8A22C7475F",
     "ActionBronsonEarlSweatshirt_Toronto_FB_1200x628.jpg", False),
    ("bbno$", "", "2021-12-12", "Door Three", "Toronto",
     "https://www.doorthree.ca/reservations/", "IMG_0600.jpeg", False),
    ("Killy", "", "2021-12-07", "London Music Hall", "London",
     "https://admitone.com/events/killy-london-7491566", "11x17(1).jpg", False),
    ("Killy", "", "2021-12-04", "Guelph Concert Theatre", "Guelph",
     "https://admitone.com/events/killy-guelph-7491558", "11x17.jpg", False),
    ("Killy", "", "2021-12-03", "The Grand", "Sudbury",
     "https://www.badhabitsentertainment.com/upcoming-events", "unnamed.jpg", False),
    ("Killy", "", "2021-12-02", "The Brass Monkey", "Ottawa",
     "https://www.eventbrite.com/e/killy-live-in-ottawa-tickets-175547606617",
     "KILLY-CANADA-TOUR-SQUARE-ADMAT.jpg", False),
    ("OHGEESY", "", "2021-11-19", "The Axis Club", "Toronto",
     "https://www.ticketweb.ca/event/ohgeesy-the-axis-club-formerly-the-tickets/11334155",
     "OHGEESY_Header.jpg", False),
    ("J.I.", "", "2021-10-20", "Queen Elizabeth Theatre", "Toronto",
     "https://www.ticketweb.ca/event/ji-queen-elizabeth-theatre-tickets/11020485",
     "J.I._Header.jpg", False),
    ("J.I.", "Afterparty", "2021-10-20", "Mister Wolf", "Toronto",
     "http://mrwolftoronto.com/", "senor_wolf_ji_1.JPEG", False),
    ("Roy Woods", "", "2021-10-17", "Marquee Ballroom", "Halifax",
     "https://www.showpass.com/roywoods-2/",
     "Screenshot-2021-10-04-at-11-36-58-Event-ROY-WOODS---HALIFAX-(SUNDAY)---Tickets-Front-Left-Inc.png", False),
    ("Roy Woods", "", "2021-10-16", "Marquee Ballroom", "Halifax",
     "https://www.showpass.com/roy-woods-halifax/",
     "ROY-WOODS-BANNER-(1)-1.png", False),
    ("IDK", "", "2021-10-15", "Williwaw Social", "Anchorage",
     "https://www.eventbrite.com/e/idk-tickets-174077669997", "IDK_FinalOnline.jpg", False),
    ("The Halluci Nation", "Hopscotch", "2021-09-25", "Grand Parade", "Halifax",
     "https://www.facebook.com/events/1209774705874561/",
     "Facebook-Banner-copy_HOPSCOTCH_2021.png", False),
    ("Charlotte Day Wilson, DVSN & Roy Woods", "CityFolk RBC Bluesfest", "2021-09-16",
     "Mavericks", "Ottawa", "https://cityfolkfestival.com/",
     "CityFolk-Facebook-TimelinePage.png", False),
    ("dvsn", "", "2021-08-22", "Midway", "Edmonton",
     "https://www.ticketweb.ca/event/dvsn-live-midway-tickets/11233815",
     "DVSN_Live_Edmonton_Facebook_Event.jpg", False),
    ("dvsn", "", "2021-08-21", "The Palace Theatre", "Calgary",
     "https://www.ticketweb.ca/event/dvsn-live-the-palace-theatre-tickets/11236085",
     "DVSN_Live_Calgary_Facebook_Event.jpg", False),
    ("Dolo In Da Cut", "", "2021-08-20", "The Luxx", "Edmonton",
     "https://theluxx.ca/", "Aug18-Dolo-1x1-Square.png", False),
    ("Night Lovell", "MURAL", "2021-08-14", "MURAL", "Montreal",
     "https://www.showpass.com/night-lovell-avec-skiifall-et-invites-en-collaboration-avec-johnnie-walker/",
     "nightlovell-bannersize.jpg", False),
    ("dvsn", "MURAL", "2021-08-12", "MURAL", "Montreal",
     "https://www.showpass.com/spectacle-douverture-de-mural-dvsn-high-klassified-et-invites/",
     "dvsn-banner.jpg", False),
    ("Killy, 88Glam & More", "Summer Block Party", "2021-07-02", "Union Hall", "Edmonton",
     "https://www.ticketweb.ca/?q=blockparty", "facebook-event.jpg", False),
    ("DUCKWRTH", "A SuperGood Night (Virtual)", "2020-10-27", "Moonlight Rollerway (Virtual)",
     "Los Angeles", "https://duckwrth.live/?affiliate=1d63089fdf5c5562",
     "duck_announce.png", False),
    ("Roy Woods w/ Savannah Re", "Facebook Live", "2020-09-19", "Phi Centre", "Montreal",
     "https://www.facebook.com/events/1693733047443751/",
     "119153959_1851953918276188_6728661146421369233_o.jpg", False),
    ("Audrey Mika", "", "2020-03-12", "Jasper Dandy", "Toronto",
     "https://www.ticketweb.ca/event/audrey-mika-jasper-dandy-tickets/10286005?pl=embrace",
     "audreymika_fb-2.jpg", True),
    ("bbno$", "", "2020-03-10", "Mod Club Theatre", "Toronto",
     "https://www.ticketweb.ca/event/bbno-the-velvet-underground-tickets/9986095?pl=embrace",
     "bbno_fb.jpg", True),
    ("Free Nationals", "", "2020-03-06", "Velvet Underground", "Toronto",
     "https://www.ticketweb.ca/event/the-free-nationals-the-velvet-underground-tickets/10423195?pl=embrace",
     "freenationals_fb.jpg", True),
    ("Cam'ron", "Purple Haze 15 Year Anniversary Tour", "2020-03-01", "Barrymore's", "Ottawa",
     "https://www.eventbrite.ca/e/camron-purple-haze-2-15-year-anniversary-tour-live-in-ottawa-tickets-83860451869",
     "F34675F0-566C-40AB-ABA7-3F9D8380DC73.jpeg", False),
    ("Lund & guccihighwaters", "", "2020-03-01", "Velvet Underground", "Toronto",
     "https://www.ticketweb.ca/event/lund-guccihighwaters-the-velvet-underground-tickets/10104305?pl=embrace",
     "lundgucci_fb.jpg", False),
    ("070 Shake", "Afterparty", "2020-02-29", "Apt 200", "Montreal",
     "https://apt200.com/montreal", "070shake_mtl.jpg", False),
    ("Kenny Glasgow", "Quart De Nuit", "2020-02-29", "Hide + Seek", "Halifax",
     "https://www.facebook.com/events/883902692041795/",
     "83232994_639111650176783_3811312111129198592_n.jpg", False),
    ("Cam'ron", "", "2020-02-29", "Th\u00e9\u00e2tre Fairmount", "Montreal",
     "https://www.facebook.com/events/842422002884029/",
     "83173425_10157073010292224_8882356465390583808_o.jpg", False),
    ("Elliot Moss", "", "2020-02-29", "Velvet Underground", "Toronto",
     "https://www.ticketweb.ca/event/elliot-moss-derover-the-velvet-underground-tickets/10060705?pl=embrace",
     "elliotmoss_fb.jpg", False),
]

# KYBBA (Fortune Sound Club, Vancouver) omitted — date unconfirmed.
EVENTS_UPCOMING = [
    ("Night Lovell", "", "2026-11-29", "TBD", "Vancouver", "", "", False),
    ("Pouya", "", "2026-11-10", "Mod Club", "Toronto", "", "", False),
    ("KWN", "", "2026-10-29", "TBD", "Toronto", "", "", False),
    ("Night Lovell", "", "2026-12-19", "MTELUS", "Montreal", "", "", False),
    ("Night Lovell", "", "2026-12-20", "HISTORY", "Ottawa",
     "https://www.ticketmaster.ca/event/31006538DF999F7C", "", False),
    ("Night Lovell", "", "2026-12-22", "Danforth Music Hall", "Toronto", "", "", False),
]


def render(artist, title, date, venue, city, ticket, flyer, sold_out, manifest):
    # validate date
    datetime.strptime(date, "%Y-%m-%d")
    img = ""
    if flyer:
        if flyer in manifest:
            img = "/img/events/" + flyer
        else:
            print("  MISSING IMAGE (left blank): %s" % flyer)
    lines = ["---"]
    lines.append("artist: %s" % yq(artist))
    lines.append("title: %s" % yq(title))
    lines.append("city: %s" % yq(city))
    lines.append("venue: %s" % yq(venue))
    lines.append("date: %s" % date)
    lines.append("image: %s" % yq(img))
    lines.append("ticket_link: %s" % yq(ticket))
    lines.append("sold_out: %s" % ("true" if sold_out else "false"))
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def main():
    os.makedirs(EVDIR, exist_ok=True)
    manifest = set(os.listdir(IMGDIR)) if os.path.isdir(IMGDIR) else set()
    print("images in manifest: %d" % len(manifest))
    all_events = EVENTS_2025 + EVENTS_2022_2023 + EVENTS_2020_2022
    print("past events in data: %d" % len(all_events))
    seen = set()
    n = 0
    for ev in all_events + EVENTS_UPCOMING:
        fn = "%s-%s-%s.md" % (ev[2], slug(ev[0]), slug(ev[4]))
        if fn in seen and ev[1]:
            # disambiguate same-day/same-artist/same-city with the title slug
            fn = "%s-%s-%s-%s.md" % (ev[2], slug(ev[0]), slug(ev[1]), slug(ev[4]))
        if fn in seen:
            raise SystemExit("FILENAME COLLISION: " + fn)
        seen.add(fn)
        body = render(*ev, manifest)
        with open(os.path.join(EVDIR, fn), "w", encoding="utf-8") as f:
            f.write(body)
        n += 1
    print("wrote %d event files to %s" % (n, EVDIR))


if __name__ == "__main__":
    main()
