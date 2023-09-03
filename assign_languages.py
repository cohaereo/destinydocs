import json
import dateutil.parser
import pytz

LANGUAGES = [
    "en",
    "fr",
    "de",
    "it",
    "jp",
    "pt",
    "es",
    "ru",
    "pl",
    "cs",
    "ct",
    "mx",
    "ko"
]

def find_closest(time, list):
    closest = None
    time = time.replace(tzinfo=pytz.UTC)
    for m in list:
        mtime = dateutil.parser.isoparse(m['date'])
        mtime = mtime.replace(tzinfo=pytz.UTC)
        # print(mtime, time)
        if mtime == time:
            return m
        
        delta = mtime - time

        
        # print("{} -> {} = {}".format(mtime, time, delta))
        if closest == None:
            closest = m
        else:
            ctime = dateutil.parser.isoparse(closest['date'])
            ctime = ctime.replace(tzinfo=pytz.UTC)

            if abs(time-mtime) < abs(time-ctime):
                closest = m
        

    mtime = dateutil.parser.isoparse(closest['date'])
    mtime = mtime.replace(tzinfo=pytz.UTC)
    delta = mtime - time
    # print("Closest is {}".format(delta))
    return None

language_files = {}
for l in LANGUAGES:
    language_files[l] = json.load(open(f"languages/{l}.json", 'r', encoding='utf8'))

m = json.load(open("manifests_old.json", 'r', encoding='utf8'))

new_manifests = []
for dlc in m:
    new_dlc = dlc

    for i in range(0, len(dlc['manifests'])):
        m = dlc['manifests'][i]
        languages = {}

        for lang in LANGUAGES:
            t = dateutil.parser.isoparse(m['date'])
            closest = find_closest(t, language_files[lang])
            if closest != None:
                languages[lang] = closest['id']

        if len(languages) > 0:
            m['language_manifests'] = languages
        new_dlc[i] = m

    new_manifests.append(new_dlc)

open("manifests.json", 'w').write(json.dumps(new_manifests, indent=4))
