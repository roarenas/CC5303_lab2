from flask import Flask, request, jsonify
import random
import os

app = Flask(__name__)

@app.route("/random", methods=["GET"])
def random_number():
    # Read seed from query parameter
    seed = request.args.get("seed", type=int)

    # Create RNG with seed
    rng = random.Random(seed)

    # Generate random number
    number = rng.randint(1, 100)
    #number = int(rng.integers(1, 101))

    return jsonify({
        "seed": seed,
        "random_number": number
    })

if __name__ == "__main__":
    # Use PORT env variable if available, otherwise default to 5000
    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)