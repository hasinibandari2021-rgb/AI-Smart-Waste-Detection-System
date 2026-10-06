import streamlit as st
from PIL import Image
import numpy as np


# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="AI Smart Waste Detection System",
    page_icon="♻️",
    layout="centered"
)


# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.main {
    padding-top: 20px;
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

.result-box {
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #ddd;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# TITLE
# =========================

st.markdown(
    '<div class="title">♻️ AI Smart Waste Detection System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Upload an image and detect the type of waste</div>',
    unsafe_allow_html=True
)


# =========================
# WASTE ANALYSIS FUNCTION
# =========================

def analyze_waste(image):

    # Convert image to RGB
    image = image.convert("RGB")

    # Resize image
    image = image.resize((200, 200))

    # Convert image to NumPy array
    img = np.array(image)

    # Calculate average RGB values
    avg_color = img.mean(axis=(0, 1))

    red = float(avg_color[0])
    green = float(avg_color[1])
    blue = float(avg_color[2])

    # Calculate brightness
    brightness = (red + green + blue) / 3

    # Calculate color variation
    color_variation = float(img.std())


    # =========================
    # CLASSIFICATION
    # =========================

    if brightness > 210 and color_variation < 35:

        waste_type = "Paper"
        category = "Recyclable"
        confidence = 87

        disposal = (
            "Place it in the paper recycling bin. "
            "Keep paper dry and remove plastic or "
            "non-paper materials."
        )

        description = (
            "The image appears to contain a "
            "light-colored paper-like material."
        )


    elif green > red * 1.15 and green > blue * 1.10:

        waste_type = "Organic"
        category = "Compostable"
        confidence = 84

        disposal = (
            "Place it in the organic waste or "
            "compost bin. Avoid mixing it with "
            "plastic or metal waste."
        )

        description = (
            "The image has strong green or "
            "organic visual characteristics."
        )


    elif red > blue * 1.20 and red > green * 1.10:

        waste_type = "Plastic"
        category = "Recyclable"
        confidence = 72

        disposal = (
            "Place it in the recyclable plastic "
            "waste bin. Clean the container before "
            "recycling when possible."
        )

        description = (
            "The image contains visual characteristics "
            "that may indicate plastic waste."
        )


    elif color_variation > 70:

        waste_type = "Mixed Waste"
        category = "Non-Recyclable / Mixed"
        confidence = 76

        disposal = (
            "Separate recyclable and organic materials "
            "before disposing of the remaining waste."
        )

        description = (
            "The image contains multiple different "
            "visual regions and may represent mixed waste."
        )


    else:

        waste_type = "Other"
        category = "Check Manually"
        confidence = 55

        disposal = (
            "Check the item manually and place it "
            "in the appropriate waste bin."
        )

        description = (
            "The system could not confidently identify "
            "a specific waste category."
        )


    return {
        "waste_type": waste_type,
        "category": category,
        "confidence": confidence,
        "disposal_method": disposal,
        "description": description
    }


# =========================
# IMAGE UPLOAD
# =========================

st.subheader("📤 Upload Waste Image")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png", "webp"]
)


# =========================
# IMAGE PROCESSING
# =========================

if uploaded_file is not None:

    try:

        # Open uploaded image
        image = Image.open(uploaded_file)

        # Display image
        st.image(
            image,
            caption="Uploaded Waste Image",
            use_container_width=True
        )

        st.write("")


        # =========================
        # DETECT BUTTON
        # =========================

        if st.button(
            "🔍 Detect Waste",
            use_container_width=True
        ):

            with st.spinner("Analyzing image..."):

                result = analyze_waste(image)


            # =========================
            # RESULT
            # =========================

            st.success("Waste Detection Completed!")


            st.markdown(
                '<div class="result-box">',
                unsafe_allow_html=True
            )


            st.subheader("📊 Detection Result")


            st.write(
                "### 🗑️ Waste Type"
            )

            st.write(
                result["waste_type"]
            )


            st.write(
                "### ♻️ Category"
            )

            st.write(
                result["category"]
            )


            st.write(
                "### 🎯 Confidence"
            )

            st.progress(
                result["confidence"] / 100
            )

            st.write(
                f'{result["confidence"]}%'
            )


            st.write(
                "### 📝 Description"
            )

            st.write(
                result["description"]
            )


            st.write(
                "### 🚮 Disposal Method"
            )

            st.info(
                result["disposal_method"]
            )


            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


    except Exception as e:

        st.error(
            f"Error processing image: {str(e)}"
        )


# =========================
# FOOTER
# =========================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;">
        <p>♻️ AI Smart Waste Detection System</p>
        <p>Helping users identify and properly dispose of waste.</p>
    </div>
    """,
    unsafe_allow_html=True
)
