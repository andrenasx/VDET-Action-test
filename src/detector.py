import json
import torch

from transformer import getModel, getTokenizer, getMultilabelBinarizer, process_sequence, get_labels
from utils import clean_code, flatten_list, remove_duplicate_labels, get_file_methods

p_model = "./models/model.bin"
p_mlb = "./models/multilabelbinarizer.pt"

model = getModel(p_model)
tokenizer = getTokenizer()
mlb = getMultilabelBinarizer(p_mlb)


""" def section(code):
    req = request.get_json(force=True)

    list_labels = []
    list_lines = []

    code = clean_code(req['code'])
    lines = '-'.join(str(e) for e in req['lines'])

    encodings = tokenizer.encode_plus(
        code,
        add_special_tokens=False,
        return_tensors='pt')

    input_ids, attn_mask = process_sequence(encodings)

    # Stack lists so that it can be passed to the transformer
    stacked_input_ids = (torch.stack(input_ids, 0)).type(torch.LongTensor)
    stacked_attn_masks = torch.stack(attn_mask, 0)

    # Get predictions
    outputs = model(ids=stacked_input_ids, mask=stacked_attn_masks)
    labels = get_labels(mlb, outputs)

    flatten = flatten_list(labels)
    noDup_labels = remove_duplicate_labels(flatten)

    list_labels.append(noDup_labels)
    list_lines.append(lines)

    results = [{"range": t, "labels": s}
               for t, s in zip(list_lines, list_labels)]
    # print(results)
    return json.dumps(results) """


def file():
    target_file = "examples/helloworld.java" # Add the path to your file
    methods = get_file_methods(target_file)

    with open("./sarif/template.sarif") as f:
        results_sarif = json.load(f)

    results = []
    
    for method in methods:
        code = clean_code(method['code'])
        methodname = method['name']
        startline = method['startline']
        endline = method['endline']

        encodings = tokenizer.encode_plus(
            code,
            add_special_tokens=False,
            return_tensors='pt')

        input_ids, attn_mask = process_sequence(encodings)

        # Stack lists so that it can be passed to the transformer
        stacked_input_ids = (torch.stack(input_ids, 0)).type(torch.LongTensor)
        stacked_attn_masks = torch.stack(attn_mask, 0)

        # Get predictions
        outputs = model(ids=stacked_input_ids, mask=stacked_attn_masks)
        labels = get_labels(mlb, outputs)

        flatten = flatten_list(labels)
        noDup_labels = remove_duplicate_labels(flatten)

        results.append({
            "ruleId": "VDET/CWE-" + noDup_labels[0][0],
            "message": {
                "id": "default",
                "arguments": [
                    noDup_labels[0][0],
                    str(round(float(noDup_labels[0][1])*100, 2))
                ]
            },
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": "/home/andrenasx/Thesis/Action/" + target_file,
                        },
                        "region": {
                            "startLine": startline,
                            "endLine": endline,
                        }
                    }
                }
            ]

        })

    results_sarif['runs'][0].update({"results": results})

    with open("./results.sarif", "w") as f:
        json.dump(results_sarif, f, indent=2)

#! Test
if __name__ == '__main__':
    #file()
    print("Done")