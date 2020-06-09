import collections
import os
import os.path as path
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.autograd as autograd
import torchvision


class Utils:

    @staticmethod
    def format_time(seconds):
        days = int(seconds / 3600 / 24)
        seconds = seconds - days * 3600 * 24
        hours = int(seconds / 3600)
        seconds = seconds - hours * 3600
        minutes = int(seconds / 60)
        seconds = seconds - minutes * 60
        secondsf = int(seconds)
        seconds = seconds - secondsf
        millis = int(seconds * 1000)

        f = ''
        i = 1
        if days > 0:
            f += str(days) + 'D'
            i += 1
        if hours > 0 and i <= 2:
            f += str(hours) + 'h'
            i += 1
        if minutes > 0 and i <= 2:
            f += str(minutes) + 'm'
            i += 1
        if secondsf > 0 and i <= 2:
            f += str(secondsf) + 's'
            i += 1
        if millis > 0 and i <= 2:
            f += str(millis) + 'ms'
            i += 1
        if f == '':
            f = '0ms'
        return f


class ProgressBar:
    TOTAL_BAR_LENGTH = 65.
    total = 0

    def __init__(self):
        _, term_width = os.popen('stty size', 'r').read().split()
        self.term_width = int(term_width)

    def update(self, current, msg=''):
        current = current + 1
        cur_len = int(self.TOTAL_BAR_LENGTH * current / self.total)
        rest_len = int(self.TOTAL_BAR_LENGTH - cur_len) - 1

        sys.stdout.write(' [')
        for i in range(cur_len):
            sys.stdout.write('=')
        sys.stdout.write('>' if current < self.total else '')
        for i in range(rest_len):
            sys.stdout.write('.')
        sys.stdout.write('] ')

        sys.stdout.write(msg)

        for i in range(self.term_width - int(self.TOTAL_BAR_LENGTH) - len(msg) - 3):
            sys.stdout.write(' ')

        for i in range(self.term_width - int(self.TOTAL_BAR_LENGTH / 2) + len(str(self.total))):
            sys.stdout.write('\b')
        sys.stdout.write(' %d/%d ' % (current, self.total))

        if current == self.total:
            sys.stdout.write('\n')
        sys.stdout.write('\r')
        sys.stdout.flush()

    def newbar(self, total, msg=''):
        self.total = total
        self.update(-1, msg)


class Chrono:
    def __init__(self):
        self.timings = collections.OrderedDict()

    def measure(self, what):
        return Timer(lambda t: self._done(what, t))

    def _done(self, what, t):
        self.timings.setdefault(what, []).append(t)

    def remove(self, what):
        self.timings[what] = []

    def last(self, what):
        return self.timings[what][-1]

    def total(self, what):
        return sum(self.timings[what])

    def avgtime(self, what, dropfirst=False):
        timings = self.timings[what]
        if dropfirst and len(timings) > 1:
            timings = timings[1:]
        return sum(timings) / len(timings)


class Timer:
    def __init__(self, donecb):
        self.cb = donecb

    def __enter__(self):
        self.t0 = time.time()

    def __exit__(self, exc_type, exc_value, traceback):
        t = time.time() - self.t0
        self.cb(t)


class Logger:
    def __init__(self, file, header=None):
        if path.exists(file):
            self.file = open(file, 'a')
        else:
            self.file = open(file, 'w')
            if header is not None:
                self.header(header)

    def header(self, header):
        self.file.write('%s\n' % header)
        self.flush()

    def write(self, log):
        self.file.write(log)
        self.flush()

    def flush(self):
        self.file.flush()


def dataloader():
    temp_transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])

    temp_set = torchvision.datasets.CIFAR10(root='./data/', train=True, transform=temp_transform)
    mean = temp_set.data.mean(axis=(0, 1, 2)) / 255
    std = temp_set.data.std(axis=(0, 1, 2)) / 255

    transform_train = torchvision.transforms.Compose([
        torchvision.transforms.RandomHorizontalFlip(),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize(mean, std),
    ])
    transform_test = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize(mean, std),
    ])

    train_dataset = torchvision.datasets.CIFAR10(root='./data', train=True, transform=transform_train)
    test_dataset = torchvision.datasets.CIFAR10(root='./data', train=False, transform=transform_test)

    train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=128, num_workers=4, shuffle=False)
    test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=100, num_workers=4, shuffle=False)

    return train_dataset, test_dataset, train_dataloader, test_dataloader


def get_torch_vars(x, var=True):
    if torch.cuda.is_available():
        x = x.cuda()
    return autograd.Variable(x) if var else x


def imshow(img):
    npimg = img.cpu().numpy()
    plt.axis('off')
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()