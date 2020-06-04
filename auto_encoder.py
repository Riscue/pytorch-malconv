import torch
import torch.autograd.Variable as Variable
import torch.nn as nn
import torch.utils.data.DataLoader as DataLoader
import torchvision.datasets.MNIST as MNIST
import torchvision.transforms as transforms


class AutoEncoder(nn.Module):
    def __init__(self):
        super(AutoEncoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(28 * 28, 256),
            nn.ReLU(True),
            nn.Linear(256, 64),
            nn.ReLU(True))
        self.decoder = nn.Sequential(
            nn.Linear(64, 256),
            nn.ReLU(True),
            nn.Linear(256, 28 * 28),
            nn.Sigmoid())

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x


def main():
    num_epochs = 200
    batch_size = 128
    learning_rate = 1e-3

    img_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda tensor: min_max_normalization(tensor, 0, 1)),
        transforms.Lambda(lambda tensor: torch.round(tensor))
    ])

    dataset = MNIST('./data', transform=img_transform, download=True)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = AutoEncoder().cuda()
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-5)

    for epoch in range(num_epochs):
        loss = ''
        mse_loss = ''
        for data in dataloader:
            img, _ = data
            img = img.view(img.size(0), -1)
            img = Variable(img).cuda()

            output = model(img)
            loss = criterion(output, img)
            mse_loss = nn.MSELoss()(output, img)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f'epoch [{epoch + 1}/{num_epochs}], loss:{loss.data:.4f}, MSE_loss:{mse_loss.data:.4f}')

    torch.save(model.state_dict(), './sim_autoencoder.pth')


def min_max_normalization(tensor, min_value, max_value):
    min_tensor = tensor.min()
    tensor = (tensor - min_tensor)
    max_tensor = tensor.max()
    tensor = tensor / max_tensor
    tensor = tensor * (max_value - min_value) + min_value
    return tensor


main()
