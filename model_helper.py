from PIL import Image
import torch
from torch import nn
from torchvision import models, transforms

# ✅ 16 Class labels for fruit freshness
class_names = [
    'F_Banana', 'F_Lemon', 'F_Lulo', 'F_Mango', 
    'F_Orange', 'F_Strawberry', 'F_Tamarillo', 'F_Tomato',
    'S_Banana', 'S_Lemon', 'S_Lulo', 'S_Mango',
    'S_Orange', 'S_Strawberry', 'S_Tamarillo', 'S_Tomato'
]

trained_model = None  # Global variable to hold the loaded model

# ✅ Custom ResNet50 model
class FreshnessResNet(nn.Module):
    def __init__(self, num_classes=16, dropout_rate=0.3):
        super().__init__()
        self.model = models.resnet50(weights='DEFAULT')
        
        # Freeze all layers initially
        for param in self.model.parameters():
            param.requires_grad = False
        
        # Unfreeze last block (layer4) + FC for fine-tuning
        for param in self.model.layer4.parameters():
            param.requires_grad = True
        
        # Replace final classification layer
        in_features = self.model.fc.in_features
        self.model.fc = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(in_features, num_classes)
        )
    
    def forward(self, x):
        return self.model(x)

# ✅ Prediction function
def predict(image_path):
    # Load and convert image to RGB
    image = Image.open(image_path).convert("RGB")
    
    # Transform for ResNet50
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    # Preprocess
    image_tensor = transform(image).unsqueeze(0)
    
    global trained_model
    if trained_model is None:
        trained_model = FreshnessResNet(num_classes=len(class_names))
        trained_model.load_state_dict(torch.load("model/freshness_resnet50.pth", map_location=torch.device('cpu')))
        trained_model.eval()
    
    # Inference
    with torch.no_grad():
        output = trained_model(image_tensor)
        _, predicted_class = torch.max(output, 1)
        prediction = class_names[predicted_class.item()]
        
        # Parse result for better display
        freshness = "Fresh" if prediction.startswith("F_") else "Stale"
        fruit_type = prediction.split("_")[1]
        
        return prediction, fruit_type, freshness