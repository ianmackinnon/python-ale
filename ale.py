# -*- coding: utf-8 -*-



headings = {
    "FIELD_DELIM": {
        "name": "field_delimiter",
        "options": [
            "TABS",
            ],
        "required": True,
        },
    "VIDEO_FORMAT": {
        "name": "video_format",
        "options": [
            "NTSC",
            "PAL",
            "1080",
            ],
        "required": True,
        },
    "FILM_FORMAT": {
        "name": "film_format",
        "options": [
            "16mm",
            "35mm, 3 perf",
            "35mm, 4 perf",
            ],
        "required": False,
        },
    "AUDIO_FORMAT": {
        "name": "audio_format",
        "options": [
            "22kHz",
            "24kHz",
            "44kHz",
            "48kHz",
            ],
        "required": False,
        },
    "TAPE" : {
        "name": "tape",
        "required": False,  # Spec says this is required, but may be omitted (?)."
        },
    "FPS": {
        "name": "fps",
        "options": [
            "24",
            "25",
            "29.97",
            ],
        "required": True,
        },
    }

columns = {
    "Name": {
        "required": True,
        },
    "Tracks": {
        "required": True,
        },
    "Start": {
        "required": True,
        },
    "End": {
        "required": True,
        },
    "Duration": {},
    "Mark IN": {},
    "Mark OUT": {},
    "IN-OUT": {},
    "Tape": {},
    "Auxiliary TC1": {},
    "Video": {},
    "Color Framing": {},
    "Audio": {},
    "Disk": {},
    "Creation Date": {},
    "Camera": {},
    "Camroll": {},
    "Auxiliary TC3": {},
    "TC 24": {},
    "KN Mark OUT": {},
    "Ink Number": {},
    "Audio Format": {},
    "KN Duration": {},
    "Labroll": {},
    "Take": {},
    "Shoot Date": {},
    "Film TC": {},
    "Offline": {},
    "Lock": {},
    "Project": {},
    "KN IN-OUT": {},
    "FPS": {},
    "Sound TC": {},
    "Pullin": {},
    "Pullout": {},
    "Reel #": {},
    "KN Mark IN": {},
    "TC 25": {},
    "Auxiliary TC5": {},
    "KN Start": {},
    "Auxiliary TC4": {},
    "Perf": {},
    "Film Type": {},
    "Auxiliary TC2": {},
    "Slip": {},
    "Scene": {},
    "CFPS": {},
    "Frame": {},
    "Color": {},
    "Media File": {},
    "Modified Date": {},
    "TC 30": {},
    "Soundroll": {},
    "TapeID": {},
    "VITC": {},
    "KN End": {},
    "Auxiliary Ink": {},
    "TC 25P": {},
}



class ale(object):
    delim = "\t"

    def _read_heading(self, line):
        key, value = line.split(self.delim)
        if not key in headings:
            raise ValueError("Unknown heading: '%s'.", key)
        heading = headings[key]
        
        if heading["options"]:
            for option in heading["options"]:
                if value.lower() == option.lower():
                    setattr(self, heading['name'], option)
                    break
            else:
                raise ValueError("Unknown '%s' value: '%s'." % (key, value))
            
    def _read_column(self, line):
        if self.columns:
            raise ValueError("Columns declared more than once.")
        self.columns = line.split(self.delim)
        if len(set(self.columns)) < len(self.columns):
            raise ValueError("Column delcared more than once.")           

    def _read_data(self, line):
        data = line.split(self.delim)
        if len(data) > len(self.columns):
            raise ValueError("More data than columns: columns:%d, data:%d." % (len(self.columns), len(data)))

        if len(data) < len(self.columns):
            data += [None] * (len(self.columns) - len(data))
        self.clips.append(dict(zip(self.columns, data)))

    def __init__(self, path=None):
        self.columns = None
        for heading in headings.values():
            setattr(self, heading['name'], None)
        self.clips = []
        if path:
            self.load(path)

    def load(self, path):
        file_object = open(path, "rU")
            
        section = None
        for line in file_object.readlines():
            line = line.rstrip("\n")

            if not line.strip():
                continue

            if section == None:
                if not line.strip().lower() == "heading":
                    raise ValueError("First section should be 'Heading', not '%s'." % line)
                section = "heading"
                continue
            if section == "heading":
                if line.strip().lower() == "column":
                    for key, heading in headings.items():
                        if "required" in heading and heading["required"]:
                            if not getattr(self, heading['name']):
                                raise ValueError("Required heading '%s' missing." % key)
                    section = "column"
                    continue
                self._read_heading(line)
                continue
            if section == "column":
                if line.strip().lower() == "data":
                    for key, column in columns.items():
                        if "required" in column and column["required"]:
                            if not key in self.columns:
                                raise ValueError("Required column '%s' missing." % key)
                    section = "data"
                    continue
                self._read_column(line)
                continue
            self._read_data(line)

    def __str__(self):
        return "<ALE - %d clips>" % len(self.clips)
