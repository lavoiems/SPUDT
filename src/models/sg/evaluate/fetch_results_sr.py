import torch
from ..model import Generator, MappingNetwork
import torchvision.utils as vutils
from common.loaders.images import dataset_single


def save_image(x, ncol, filename):
    x = (x + 1) / 2
    x.clamp_(0, 1)
    vutils.save_image(x.cpu(), filename, nrow=ncol, padding=0)


def parse_args(parser):
    parser.add_argument('--state-dict-path', type=str, help='Path to the model state dict')
    parser.add_argument('--data-root-src', type=str, help='Path to the data')
    parser.add_argument('--domain', type=int, help='Domain id {0, 1}')
    parser.add_argument('--save-name', type=str, help='Name of the sample file')


@torch.no_grad()
def execute(args):
    state_dict_path = args.state_dict_path
    domain = args.domain
    name = args.save_name

    device = 'cuda'
    N = 5
    latent_dim = 16
    domain = int(domain)
    # Load model
    state_dict = torch.load(state_dict_path, map_location='cpu')
    generator = Generator(bottleneck_size=64, bottleneck_blocks=4).to(device)
    generator.load_state_dict(state_dict['generator'])
    mapping = MappingNetwork()
    mapping.load_state_dict(state_dict['mapping_network'])
    mapping.to(device)

    dataset = dataset_single(args.data_root_src)
    idxs = [0, 15, 31, 50, 60]
    data = []
    for i in range(N):
        idx = idxs[i]
        data.append(dataset[idx])
    data = torch.stack(data).to(device)

    # Infer translated images
    d_trg = torch.tensor(domain).repeat(25).long().to(device)
    z_trg = torch.cat(5*[torch.randn(1, 5, latent_dim)]).to(device)
    z_trg = z_trg.transpose(0,1).reshape(25, latent_dim)
    data = torch.cat(5*[data])
    print(z_trg.shape, data.shape)

    N, C, H, W = data.size()
    x_concat = [data]

    print(z_trg.shape, d_trg.shape)
    s_trg = mapping(z_trg, d_trg)
    print(data.shape, s_trg.shape)
    x_fake = generator(data, s_trg)
    x_concat += [x_fake]

    x_concat = torch.cat(x_concat, dim=0)
    print(x_concat[:5].shape, x_concat[N:].shape)
    results = torch.cat([x_concat[:5], x_concat[N:]])
    save_image(results, 5, f'{name}.png')
