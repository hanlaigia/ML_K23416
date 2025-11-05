import os
import pickle
import tempfile
import traceback

class FileUtil:
    @staticmethod
    def saveModel(model, filename):
        try:
            folder = os.path.dirname(filename) or "."
            os.makedirs(folder, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=folder, delete=False) as tmp:
                pickle.dump(model, tmp, protocol=pickle.HIGHEST_PROTOCOL)
                tmp.flush()
                os.fsync(tmp.fileno())
                tempname = tmp.name
            os.replace(tempname, filename)
            return True
        except Exception:
            traceback.print_exc()
            try:
                if 'tempname' in locals() and os.path.exists(tempname):
                    os.remove(tempname)
            except Exception:
                pass
            return False

    @staticmethod
    def loadModel(filename):
        try:
            if not os.path.exists(filename):
                return None
            if os.path.getsize(filename) == 0:
                return None
            with open(filename, 'rb') as f:
                model = pickle.load(f)
            return model
        except Exception:
            traceback.print_exc()
            return None
