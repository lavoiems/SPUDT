"""
Code adapted from the StarGAN v2 repository: https://github.com/clovaai/stargan-v2
"""
import os

from munch import Munch

from .train import Solver
from common.loaders.images import visda, mnist_svhn
from . import model


def subdirs(dname):
    return [d for d in os.listdir(dname)
            if os.path.isdir(os.path.join(dname, d))]


def execute(args):
    print(args)

    solver = Solver(args)

    #assert len(subdirs(args.dataset_loc)) == args.num_domains
    if args.dataset == 'visda':
        src, val, _, _ = visda(root=args.dataset_loc,
                               train_batch_size=args.train_batch_size,
                               test_batch_size=args.test_batch_size)
    elif args.dataset == 'mnist_svhn':
        src, val, _, _ = mnist_svhn(root=args.dataset_loc,
                                    train_batch_size=args.train_batch_size,
                                    test_batch_size=args.test_batch_size)
    else:
        print(f'Unsupported dataset: {args.dataset}')
    loaders = Munch(src=src,
                    ref=None,
                    val=val)
    solver.train(loaders)


def parse_args(parser):
    # model arguments
    parser.add_argument('--img_size', type=int, default=256, help='Image resolution')
    parser.add_argument('--num_domains', type=int, default=2, help='Number of domains')
    parser.add_argument('--num_classes', type=int, default=5, help='Number of classes')
    parser.add_argument('--latent_dim', type=int, default=16, help='Latent vector dimension')
    parser.add_argument('--hidden_dim', type=int, default=512,help='Hidden dimension of mapping network')
    parser.add_argument('--style_dim', type=int, default=64, help='Style code dimension')
    parser.add_argument('--n_unshared_layers', type=int, default=0, help='Style encoder number of unshared hidden layers')
    parser.add_argument('--bottleneck_size', type=int, default=64, help='Spatial dimension of the bottleneck of the generator')
    parser.add_argument('--bottleneck_blocks', type=int, default=2, help='Number of bottleneck block of the generator')
    parser.add_argument('--max_conv_dim', type=int, default=512, help='Maximum number of dim')
    parser.add_argument('--dataset', type=str, default='visda', help='Dataset name')

    # weight for objective functions
    parser.add_argument('--lambda_reg', type=float, default=1, help='Weight for R1 regularization')
    parser.add_argument('--lambda_cyc', type=float, default=10, help='Weight for cyclic consistency loss')
    parser.add_argument('--lambda_vae', type=float, default=0.1, help='Weight for style reconstruction loss')
    parser.add_argument('--lambda_vgg', type=float, default=0.1, help='Weight for style reconstruction loss')
    parser.add_argument('--lambda_gram', type=float, default=0.1, help='Weight for style reconstruction loss')

    # training arguments
    parser.add_argument('--randcrop_prob', type=float, default=0.5, help='Probabilty of using random-resized cropping')
    parser.add_argument('--total_iters', type=int, default=100000, help='Number of total iterations')
    parser.add_argument('--resume_iter', type=int, default=0, help='Iterations to resume training/testing')
    parser.add_argument('--lr', type=float, default=1e-4, help='Learning rate for D, E and G')
    parser.add_argument('--f_lr', type=float, default=1e-6, help='Learning rate for F')
    parser.add_argument('--beta1', type=float, default=0.0, help='Decay rate for 1st moment of Adam')
    parser.add_argument('--beta2', type=float, default=0.99, help='Decay rate for 2nd moment of Adam')
    parser.add_argument('--weight_decay', type=float, default=1e-4, help='Weight decay for optimizer')
    parser.add_argument('--num_outs_per_domain', type=int, default=10, help='Number of generated images per domain during sampling')

    parser.add_argument('--num_workers', type=int, default=4, help='Number of workers used in DataLoader')
    parser.add_argument('--cluster_path', type=str, default='.', help='Path to cluster model')
    parser.add_argument('--ss_path', type=str, default='.', help='Path to self-supervision model')

    # directory for training
    parser.add_argument('--dataset_loc', type=str, default='.data', help='Directory containing datasets')

    # step size
    parser.add_argument('--print_every', type=int, default=1000)
    parser.add_argument('--sample_every', type=int, default=5000)
    parser.add_argument('--save_every', type=int, default=10000)

