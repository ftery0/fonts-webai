# ml_server/train.py
import argparse

def train(dataset, epochs, batch, lr, char_embedding_size):
    print("===== Training Start =====")
    print(f"Dataset: {dataset}, Epochs: {epochs}, Batch: {batch}, LR: {lr}, Embedding: {char_embedding_size}")
    print("==========================")
    # TODO: 데이터 로딩
    # TODO: 모델 정의(GAN/CNN)
    # TODO: 학습 루프
    # TODO: 체크포인트 저장

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--char-embedding-size", type=int, default=128)
    args = parser.parse_args()

    train(
        dataset=args.dataset,
        epochs=args.epochs,
        batch=args.batch,
        lr=args.lr,
        char_embedding_size=args.char_embedding_size
    )
