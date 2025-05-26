'''
this script parses conf file [section] -> content as key value pairs of Slimparser()
'''

class SlimParser:
    def __init__(self,file):
        self.file = file
        self.headers = {}
        self.current_key = None

        #run on init
        with open(file, 'r') as f:
            text = f.read()

        lines = text.splitlines()

        # Looks for  [headers]
        for line in lines:
            line = line.strip()

            if (
                line.startswith('[')
                and line.endswith(']')
                and len(line) > 2
                and line.count('[') == 1
                and line.count(']') == 1
            ):
                section_name = line[1:-1].strip()

                if section_name:
                    self.current_key = section_name
                    self.headers[self.current_key] = []
            elif self.current_key:
                self.headers[self.current_key].append(line)


    def getHeaders(self):
        return (self.headers.keys())

    def get(self,section):
        """Returns the header"""
        return self.headers.get(section)

    def cleanSection(self, section):
        """Strips and removes empty lines, duplicates from a section."""
        if section in self.headers:
            self.headers[section] = list(set(
                    line.strip() for line in self.headers[section] if line.strip()
                    ))

        elif section not in self.headers:
            raise ValueError(f"Section '{section}' not found in headers.")

    def cleanAll(self):
        """Strips and removes empty lines, duplicates from a All the file."""
        for section in self.headers.keys():
            self.headers[section] = list(set(
                    line.strip() for line in self.headers[section] if line.strip()
                    ))
