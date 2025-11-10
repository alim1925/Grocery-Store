import json, os, re, time

class FileHandler:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.paths = {"products": os.path.join(self.data_dir, "products.json"),
                      "transactions": os.path.join(self.data_dir, "transactions.json")}
        for p in self.paths.values():
            if not os.path.exists(p):
                with open(p, 'w', encoding='utf-8') as f:
                    json.dump([], f)

    def load(self, key, default=None):
        path = self.paths.get(key)
        if not path:
            return default
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return default if default is not None else []

    def save(self, key, data):
        path = self.paths.get(key)
        if not path:
            return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print('Gagal menyimpan:', e)

class Validator:
    NAME_RE = re.compile(r'^[\w\s\-\.\,]{1,100}$', re.UNICODE)
    INT_RE = re.compile(r'^\d+$')

    @staticmethod
    def is_valid_name(s):
        return bool(Validator.NAME_RE.match(s.strip()))

    @staticmethod
    def is_valid_int(s):
        return bool(Validator.INT_RE.match(s.strip()))

def is_number(s):
    try:
        int(s)
        return True
    except Exception:
        return False

def format_money(v):
    try:
        v = int(v)
    except Exception:
        v = 0
    return f"Rp {v:,}".replace(',', '.')

def timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S')
