const API_BASE_URL = "http://127.0.0.1:5000";

const form = document.getElementById("prediction-form");
const submitButton = form.querySelector('button[type="submit"]');
const priceUsdEl = document.getElementById("price-usd");
const priceInrEl = document.getElementById("price-inr");
const resultMessageEl = document.getElementById("result-message");

const USD_TO_INR = 83;
const DATASET_SCALER = 100000;

const formatUsd = (value) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);

const formatInr = (value) =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);

const setResult = ({ prediction = null, message, error = false }) => {
  if (prediction !== null) {
    const usdValue = prediction * DATASET_SCALER;
    const inrValue = usdValue * USD_TO_INR;
    priceUsdEl.textContent = formatUsd(usdValue);
    priceInrEl.textContent = formatInr(inrValue);
  } else {
    priceUsdEl.textContent = "-";
    priceInrEl.textContent = "-";
  }
  resultMessageEl.textContent = message;
  resultMessageEl.classList.toggle("error", error);
};

const normalizePayload = (formData) =>
  Object.fromEntries(
    Array.from(formData.entries()).map(([key, value]) => [key, Number(value)])
  );

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = normalizePayload(new FormData(form));
  setResult({ prediction: null, message: "Predicting..." });
  submitButton.disabled = true;
  submitButton.textContent = "Predicting...";

  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const body = await response.json();
    if (!response.ok) {
      throw new Error(body.error || "Prediction failed");
    }

    setResult({
      prediction: body.prediction,
      message: "Prediction ready !",
    });
  } catch (error) {
    setResult({
      prediction: null,
      message: error.message,
      error: true,
    });
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Predict price";
  }
});

setResult({
  prediction: null,
  message: "Fill out the form to see a prediction.",
});
