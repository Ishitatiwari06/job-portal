const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const dns = require("node:dns");
require("dotenv").config();

const app = express();
const port = process.env.PORT || 5000;
const mongoUri = process.env.MONGO_URI;

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
    res.send("Job Portal Backend is running");
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});

const connectMongo = async () => {
    try {
        await mongoose.connect(mongoUri);
        console.log("MongoDB connected");
    } catch (error) {
        if (error.code !== "ECONNREFUSED" || error.syscall !== "querySrv") {
            console.error("MongoDB connection failed:", error);
            return;
        }

        console.warn("MongoDB SRV lookup was refused; retrying with public DNS");
        dns.setServers(["1.1.1.1", "8.8.8.8"]);

        try {
            await mongoose.connect(mongoUri);
            console.log("MongoDB connected");
        } catch (retryError) {
            console.error("MongoDB connection failed after DNS retry:", retryError);
        }
    }
};

connectMongo();