# ==========================================
# Westbank Digital Market - Streamlit App
# ==========================================

import streamlit as st
import pandas as pd
import os

# ================================
# PAGE CONFIGURATION
# ================================
st.set_page_config(
    page_title="Westbank Digital Market",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================
# CREATE DATA FILES IF NOT EXIST
# ================================
if not os.path.exists("products.csv"):
    products = pd.DataFrame({
        "ID": [1, 2, 3],
        "Name": ["Fresh Tomatoes", "Organic Maize", "Farm Eggs"],
        "Price": [2.50, 1.20, 0.50],
        "Stock": [50, 100, 200],
        "Image": [
            "https://images.unsplash.com/photo-1617196030429-1d395cce0421?auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1617200206167-8df0aa8b1cf1?auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1565958011701-44d29c3e1653?auto=format&fit=crop&w=400&q=80"
        ]
    })
    products.to_csv("products.csv", index=False)
else:
    products = pd.read_csv("products.csv")

if not os.path.exists("orders.csv"):
    orders = pd.DataFrame(columns=["Name", "Quantity", "Total"])
    orders.to_csv("orders.csv", index=False)
else:
    orders = pd.read_csv("orders.csv")

# ================================
# SIDEBAR - MENU
# ================================
menu = ["Home", "Cart", "Admin Panel"]
choice = st.sidebar.selectbox("Menu", menu)

# ================================
# HOME PAGE
# ================================
if choice == "Home":
    st.title("🛒 Welcome to Westbank Digital Market!")
    st.markdown(
        "<h3 style='color:green'>Fresh, Local & Sustainable Products!</h3>", unsafe_allow_html=True
    )

    # Promotion Banner
    st.image(
        "https://images.unsplash.com/photo-1589923188900-6b2cf0574f65?auto=format&fit=crop&w=1200&q=80",
        use_column_width=True
    )
    st.markdown("<h4 style='color:orange'>🔥 Limited Time Offer: Buy 3 get 1 Free on Farm Eggs!</h4>", unsafe_allow_html=True)

    st.markdown("---")

    # Display Products in Columns
    for i, row in products.iterrows():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.image(row["Image"], width=150)
        with col2:
            st.subheader(row["Name"])
            st.write(f"Price: ${row['Price']}")
            st.write(f"Stock: {row['Stock']}")
        with col3:
            qty = st.number_input(f"Quantity {row['ID']}", min_value=0, max_value=int(row["Stock"]), value=0)
            if st.button(f"Add to Cart {row['ID']}"):
                if qty > 0:
                    orders = pd.read_csv("orders.csv")
                    total = qty * row["Price"]
                    orders = orders.append({"Name": row["Name"], "Quantity": qty, "Total": total}, ignore_index=True)
                    orders.to_csv("orders.csv", index=False)
                    st.success(f"✅ {qty} x {row['Name']} added to cart!")
                else:
                    st.warning("Please select quantity greater than 0")

# ================================
# CART PAGE
# ================================
elif choice == "Cart":
    st.title("🛍️ Your Cart")
    orders = pd.read_csv("orders.csv")
    if orders.empty:
        st.info("Your cart is empty. Add products from Home page.")
    else:
        st.dataframe(orders)
        if st.button("Checkout"):
            st.success("🎉 Thank you for your purchase!")
            # Reduce stock
            for i, item in orders.iterrows():
                products.loc[products["Name"] == item["Name"], "Stock"] -= item["Quantity"]
            products.to_csv("products.csv", index=False)
            # Clear orders
            orders = pd.DataFrame(columns=["Name", "Quantity", "Total"])
            orders.to_csv("orders.csv", index=False)

# ================================
# ADMIN PANEL
# ================================
elif choice == "Admin Panel":
    st.title("🔧 Admin Panel")
    st.subheader("Add New Product")
    with st.form("Add Product"):
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0.0)
        stock = st.number_input("Stock Quantity", min_value=0)
        image = st.text_input("Image URL")
        submitted = st.form_submit_button("Add Product")
        if submitted:
            new_id = products["ID"].max() + 1 if not products.empty else 1
            products = products.append({"ID": new_id, "Name": name, "Price": price, "Stock": stock, "Image": image}, ignore_index=True)
            products.to_csv("products.csv", index=False)
            st.success(f"✅ Product {name} added successfully!")

    st.markdown("---")
    st.subheader("Current Inventory")
    st.dataframe(products)


