import math, random

def bucket(N, n, inputs_tuple, weights_tuple):
    if(len(inputs_tuple) == 0):
        return []
    else:
        inputs = list(inputs_tuple)
        weights = list(weights_tuple)

        prns = [wi/sum(weights) for wi in weights]
        ceilings = [math.ceil(N*prn) for prn in prns]
        ceilings.append(N - sum(ceilings[:-1]))
        del ceilings[-2]

        outputs = [[] for item in inputs]
        for output in outputs:
            inp = inputs[outputs.index(output)]
            if(len(inp) >= ceilings[outputs.index(output)]):
                output.extend(inp[:ceilings[outputs.index(output)]])
                inputs[outputs.index(output)][:] = inputs[outputs.index(output)][ceilings[outputs.index(output)]:]
            else:
                output.extend(inp[:])
                inputs[outputs.index(output)] = []
                rem_N = ceilings[outputs.index(output)] - len(inp[:])
                output.extend(bucket(rem_N, n, tuple(inputs[outputs.index(output)+1:]), tuple(weights[outputs.index(output)+1:])))
        final_list = []
        for output in outputs:
            final_list += output

        f = []
        roofs = [math.ceil(len(output)/N*n) for output in outputs]
        roofs.append(n - sum(roofs[:-1]))
        del roofs[-2]

        pages = math.ceil(N/n)

        for page in range(pages):
            temp = []
            for output in outputs:
                temp += output[:roofs[outputs.index(output)]]
            random.shuffle(temp)
            f = f + temp
            for output in outputs:
                output[:] = output[roofs[outputs.index(output)]:]
        
        return f