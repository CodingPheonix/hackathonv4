import { useRef, useState } from "react";

export default function OTPInput({ length = 6, onComplete }) {
    const [otp, setOtp] = useState(new Array(length).fill(""));
    const inputsRef = useRef([]);

    const handleChange = (value, index) => {
        if (!/^\d?$/.test(value)) return; 

        const newOtp = [...otp];
        newOtp[index] = value;
        setOtp(newOtp);

        // Move to next input
        if (value && index < length - 1) {
            inputsRef.current[index + 1].focus();
        }

        // Trigger onComplete when filled
        if (newOtp.every((digit) => digit !== "") && onComplete) {
            onComplete(newOtp.join(""));
        }
    };

    const handleKeyDown = (e, index) => {
        if (e.key === "Backspace" && !otp[index] && index > 0) {
            inputsRef.current[index - 1].focus();
        }
    };

    const handlePaste = (e) => {
        e.preventDefault();
        const pastedData = e.clipboardData.getData("text").trim();

        if (new RegExp(`^\\d{${length}}$`).test(pastedData)) {
            const newOtp = pastedData.split("");
            setOtp(newOtp);

            newOtp.forEach((digit, index) => {
                inputsRef.current[index].value = digit;
            });

            if (onComplete) {
                onComplete(pastedData);
            }

            inputsRef.current[length - 1].focus();
        }
    };

    return (
        <div className="flex gap-3 justify-center">
            {otp.map((digit, index) => (
                <input
                    key={index}
                    type="text"
                    inputMode="numeric"
                    maxLength="1"
                    value={digit}
                    ref={(el) => (inputsRef.current[index] = el)}
                    onChange={(e) => handleChange(e.target.value, index)}
                    onKeyDown={(e) => handleKeyDown(e, index)}
                    onPaste={handlePaste}
                    className="w-12 h-14 text-center text-xl font-semibold 
                     border border-gray-300 rounded-lg 
                     focus:outline-none focus:ring-2 focus:ring-blue-500 
                     focus:border-blue-500 transition"
                />
            ))}
        </div>
    );
}