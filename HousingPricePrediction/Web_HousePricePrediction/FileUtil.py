import pickle
import joblib
import os

class FileUtil:
    @staticmethod
    def savemodel(model, filename):
        """
        Lưu model vào file (hỗ trợ .pkl hoặc .zip)
        """
        try:
            # Nếu là file zip thì dùng joblib (nén tốt hơn)
            if filename.endswith(".zip"):
                joblib.dump(model, filename)
            else:
                with open(filename, 'wb') as f:
                    pickle.dump(model, f)
            print(f"✅ Model saved successfully: {filename}")
        except Exception as e:
            print("❌ Error while saving model:", e)

    @staticmethod
    def loadmodel(filename):
        """
        Đọc model đã lưu (tự động nhận dạng .pkl hoặc .zip)
        """
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError(f"Model file not found: {filename}")

            if filename.endswith(".zip"):
                model = joblib.load(filename)
            else:
                with open(filename, 'rb') as f:
                    model = pickle.load(f)

            print(f"Model loaded successfully: {filename}")
            return model
        except Exception as e:
            print("Error while loading model:", e)
            return None
