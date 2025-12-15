import argparse
import random
import time

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def get_loaders(data_root: str, batch_size: int, num_workers: int):
    tfm = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    train_set = torchvision.datasets.MNIST(root=data_root, train=True, download=True, transform=tfm)
    test_set = torchvision.datasets.MNIST(root=data_root, train=False, download=True, transform=tfm)

    train_loader = DataLoader(
        train_set,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )
    test_loader = DataLoader(
        test_set,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )
    return train_loader, test_loader


class MLP(nn.Module):
    def __init__(self, hidden, activation: str, dropout: float):
        super().__init__()

        act = activation.strip().lower()
        if act == "relu":
            act_layer = nn.ReLU
        elif act in ("sigmoid", "logistic"):
            act_layer = nn.Sigmoid
        elif act == "tanh":
            act_layer = nn.Tanh
        else:
            raise ValueError("activation must be relu/sigmoid/tanh")

        layers = []
        prev = 28 * 28
        for w in hidden:
            layers.append(nn.Linear(prev, w))
            layers.append(act_layer())
            if dropout and dropout > 0:
                layers.append(nn.Dropout(p=dropout))
            prev = w
        layers.append(nn.Linear(prev, 10))

        self.net = nn.Sequential(*layers)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        return self.net(x)


def train_eval(hidden, activation, dropout, lr, epochs, train_loader, test_loader, device, tag: str):
    model = MLP(hidden=hidden, activation=activation, dropout=dropout).to(device)
    crit = nn.CrossEntropyLoss()
    opt = optim.Adam(model.parameters(), lr=lr)

    best_acc = 0.0
    best_epoch = 0
    t0 = time.time()

    for ep in range(1, epochs + 1):
        model.train()
        tr_loss = 0.0
        tr_ok = 0
        tr_n = 0

        for x, y in train_loader:
            x = x.to(device, non_blocking=True)
            y = y.to(device, non_blocking=True)

            opt.zero_grad(set_to_none=True)
            out = model(x)
            loss = crit(out, y)
            loss.backward()
            opt.step()

            tr_loss += float(loss.item()) * y.size(0)
            tr_ok += int((out.argmax(1) == y).sum().item())
            tr_n += int(y.size(0))

        model.eval()
        te_loss = 0.0
        te_ok = 0
        te_n = 0
        with torch.no_grad():
            for x, y in test_loader:
                x = x.to(device, non_blocking=True)
                y = y.to(device, non_blocking=True)
                out = model(x)
                loss = crit(out, y)
                te_loss += float(loss.item()) * y.size(0)
                te_ok += int((out.argmax(1) == y).sum().item())
                te_n += int(y.size(0))

        tr_loss /= max(1, tr_n)
        te_loss /= max(1, te_n)
        tr_acc = tr_ok / max(1, tr_n)
        te_acc = te_ok / max(1, te_n)

        if te_acc > best_acc:
            best_acc = te_acc
            best_epoch = ep

        print(
            f"{tag} ep {ep:02d}/{epochs} | "
            f"train {tr_loss:.4f} {tr_acc*100:.2f}% | "
            f"test {te_loss:.4f} {te_acc*100:.2f}%"
        )

    return {
        "best_acc": best_acc,
        "best_epoch": best_epoch,
        "seconds": time.time() - t0
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--data_root", type=str, default="./data")
    p.add_argument("--batch_size", type=int, default=64)
    p.add_argument("--num_workers", type=int, default=2)
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--dropout", type=float, default=0.0)
    args = p.parse_args()

    set_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device:", device)

    train_loader, test_loader = get_loaders(args.data_root, args.batch_size, args.num_workers)

    arch_list = [
        ("arch_1x128_relu", [128], "relu"),
        ("arch_2x128_64_relu", [128, 64], "relu"),
        ("arch_3x256_128_64_relu", [256, 128, 64], "relu"),
    ]

    arch_results = []
    for name, hidden, act in arch_list:
        r = train_eval(hidden, act, args.dropout, args.lr, args.epochs, train_loader, test_loader, device, name)
        arch_results.append((name, hidden, act, r["best_acc"], r["best_epoch"], r["seconds"]))

    print("\nАрхитектуры:")
    for name, hidden, act, best_acc, best_ep, sec in arch_results:
        print(f"{name} hidden={hidden} act={act} best={best_acc*100:.2f}% (ep {best_ep}) time={sec:.1f}s")

    best_arch = max(arch_results, key=lambda x: x[3])
    print("Лучшая архитектура:", best_arch[0], f"{best_arch[3]*100:.2f}%")
    print("")

    base_hidden = [128, 64]
    act_list = [
        ("act_relu", base_hidden, "relu"),
        ("act_sigmoid", base_hidden, "sigmoid"),
        ("act_tanh", base_hidden, "tanh"),
    ]

    act_results = []
    for name, hidden, act in act_list:
        r = train_eval(hidden, act, args.dropout, args.lr, args.epochs, train_loader, test_loader, device, name)
        act_results.append((name, hidden, act, r["best_acc"], r["best_epoch"], r["seconds"]))

    print("\nАктивации:")
    for name, hidden, act, best_acc, best_ep, sec in act_results:
        print(f"{name} hidden={hidden} act={act} best={best_acc*100:.2f}% (ep {best_ep}) time={sec:.1f}s")

    best_act = max(act_results, key=lambda x: x[3])
    print("Лучшая активация:", best_act[2], f"{best_act[3]*100:.2f}%")
    print("")

    print("Выводы:")
    print(f"- По архитектурам лучше: {best_arch[0]} (best_test_acc={best_arch[3]*100:.2f}%).")
    print(f"- По активациям лучше: {best_act[2]} (best_test_acc={best_act[3]*100:.2f}%).")
    print("- Результат зависит от epochs/lr/dropout; для честного сравнения их фиксируют между экспериментами.")
