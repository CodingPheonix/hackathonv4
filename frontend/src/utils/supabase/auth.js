import supabase from "./supabase"

export async function signInWithOtp({ email }) {
    const { data, error } = await supabase.auth.signInWithOtp({
        email: email,
        options: {
            shouldCreateUser: true,
        },
    })

    return { data, error }
}

export async function veriyOTP({ email, token }) {
    const {
        data: { session },
        error,
    } = await supabase.auth.verifyOtp({
        email: email,
        token: token,
        type: 'email',
    })
}

export async function signInWithGoogle() {
    const { data, error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
    })

    return { data, error }
}

export async function logOut() {
    await supabase.auth.signOut();
}