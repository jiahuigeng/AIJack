from torch import nn

from ..core import BaseClient


class FedGEMSClient(BaseClient):
    def __init__(
        self,
        model,
        user_id=0,
        lr=0.1,
        base_loss_func=nn.CrossEntropyLoss(),
        kldiv_loss_func=nn.KLDivLoss(),
        epsilon=0.75,
    ):
        super(FedGEMSClient, self).__init__(model, user_id=user_id)
        self.lr = lr
        self.predicted_values_of_server = None
        self.base_loss_func = base_loss_func
        self.kldiv_loss_func = kldiv_loss_func
        self.epsilon = epsilon

    def upload(self, x):
        return self(x)

    def download(self, predicted_values_of_server):
        self.predicted_values_of_server = predicted_values_of_server

    def culc_loss_on_public_dataset(self, idx, y_pred, y):
        y_pred_server = self.predicted_values_of_server[idx]
        base_loss = self.epsilon * self.base_loss_func(y_pred, y)
        kl_loss = (1 - self.epsilon) * self.kldiv_loss_func(
            y_pred_server.softmax(dim=-1).log(), y_pred.softmax(dim=-1)
        )
        return base_loss + kl_loss
