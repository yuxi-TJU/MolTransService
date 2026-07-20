# Workflow Assessment Ablation Study

This directory contains the workflow assessment ablation study comparing two experimental conditions:

- Condition A: MST Manual only.
- Condition B: MST Manual plus retrieved examples (top 3 by default).

## Enter the Study Directory

From the repository root, run:

```bash
cd mol_trans_service/protocol_generator/ablation_study_for_workflow_assessment/
```

## Run the Experiments

Run Condition A with Gemini 2.5 Pro:

```bash
python batch_test.py -c cond_a -m gemini-2.5-pro -r 1
```

Run Condition B with Llama 3.1 70B:

```bash
python batch_test.py -c cond_b -m llama-3.1-70b -r 1
```

Set the number of retrieved examples to five:

```bash
python batch_test.py -c cond_b -m llama-3.1-70b --top-k 5
```

Run only the first three test cases:

```bash
python batch_test.py -c cond_a -n 3
```

Run three cases in parallel:

```bash
python batch_test.py -c cond_a --parallel 3
```

Retry failed cases:

```bash
python batch_test.py -c cond_a -r 1 --retry-failed
```

## Save Generated Prompts

Use `--save-prompt` to save one Markdown prompt file for each case:

```bash
python batch_test.py -c cond_a -m gemini-2.5-pro --save-prompt
```

Prompt saving is disabled by default:

```bash
python batch_test.py -c cond_a -m gemini-2.5-pro
```

## Example: Repeated Condition B Run

The following command runs test case 7 five times with Gemini 2.5 Pro and saves the generated prompts:

```bash
python batch_test.py -c cond_b -m gemini-2.5-pro -s 7 -n 1 -r 5 --save-prompt
```
