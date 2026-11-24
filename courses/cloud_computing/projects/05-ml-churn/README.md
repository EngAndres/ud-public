# 05 - Custom ML with SageMaker (Python)

Source: [../../guides/05-custom-ml-sagemaker.md](../../guides/05-custom-ml-sagemaker.md)

The data in `data/` is already generated (run `python3 make_data.py` to regenerate it). The deployment has three stages, because the endpoint needs a trained model:

- **Stage A:** data bucket, roles, and a weekly retraining Lambda (no endpoint yet).
- **Stage B:** train the first model with the AWS CLI and check the validation AUC gate (Section 6 of the guide has the commands).
- **Stage C:** deploy the endpoint with the model artifact.

## Stage A

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap                # once per account and region
cdk deploy
```

## Stage C (after training in Stage B)

```bash
cdk deploy -c modelDataUrl=<S3ModelArtifactsValue> -c modelVersion=v1
```

## Clean up

The endpoint bills by the hour. Destroy the stack when you finish:

```bash
cdk destroy MlChurnStack
aws sagemaker list-endpoints
```
