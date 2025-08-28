import streamlit as st
import pandas as pd
import core.pdf_utils as pdf_utils
import core.ocr_utils as ocr_utils
import core.text_utils as text_utils
import core.gpt_extractor as gpt_extractor

st.set_page_config(page_title="Invoice Parser", layout="centered")
st.title("*Test Application..*")

uploaded_pdf = st.file_uploader("Upload your invoice PDF", type=["pdf"])

if uploaded_pdf:
    st.success(" PDF uploaded successfully!")

    try:
        images = pdf_utils.pdf_to_images(uploaded_pdf)
        st.success(f" PDF converted to {len(images)} image(s)")

        all_items = []

        for page_num, image in enumerate(images):
            st.info(f" Processing page {page_num + 1}...")

            page_text = ocr_utils.extract_text_from_images([image])
            cleaned_text = text_utils.clean_text(page_text)
            structured_items = gpt_extractor.extract_invoice_items(cleaned_text)

            if isinstance(structured_items, list):
                all_items.extend(structured_items)
                st.success(f" Page {page_num + 1} processed successfully")
            else:
                st.warning(f" GPT extraction failed on page {page_num + 1}")
                st.code(structured_items.get("raw_output", ""), language="json")

        if all_items:
            df = pd.DataFrame(all_items)

            # Type conversion
            df["Quantity"] = pd.to_numeric(df["Quantity"], errors='coerce').fillna(0).astype(int)
            df["Price"] = pd.to_numeric(df["Price"], errors='coerce').fillna(0.0).astype(float)

            # Set index to start from 1
            df.index = range(1, len(df) + 1)

            # Calculate total
            total_price = df["Price"].sum()

            # Create total row (no index)
            total_row = pd.DataFrame([{
                "Item Name": "TOTAL",
                "Quantity": "",
                "Price": total_price
            }])
            total_row.index = ['']  # No index for total

            # Final table
            df_final = pd.concat([df, total_row])

            # Display in Streamlit
            st.success(" Extraction complete! Displaying data below:")
            st.dataframe(df_final)

            # Prepare CSV (remove index entirely)
            csv = df_final.reset_index(drop=True).to_csv(index=False).encode("utf-8")
            st.download_button(" Download CSV", data=csv, file_name="invoice_items_with_total.csv", mime="text/csv")
        else:
            st.error(" No structured data could be extracted.")

    except Exception as e:
        st.error(f" Error occurred: {e}")
