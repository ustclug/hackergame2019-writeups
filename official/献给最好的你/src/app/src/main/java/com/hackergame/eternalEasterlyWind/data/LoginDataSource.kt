package com.hackergame.eternalEasterlyWind.data

import android.util.Base64
import android.util.Log
import com.hackergame.eternalEasterlyWind.data.model.LoggedInUser
import java.io.IOException

/**
 * Class that handles authentication w/ login credentials and retrieves user information.
 */
class LoginDataSource {

    fun login(password: String): Result<LoggedInUser> {
        try {
            // TODO: handle loggedInUser authentication
            val passwordByteArray = password.toByteArray()

            val password1String = Base64.encodeToString(passwordByteArray, Base64.NO_WRAP)
            val charIterator = password1String.iterator()
            var output = ""
            for (char in charIterator) {
                output += if (char.isUpperCase()) {
                    char.toLowerCase()
                } else if (char.isLowerCase()) {
                    char.toUpperCase()
                } else {
                    char
                }
            }
            Log.d("pass1", output)
            fun byteArrayOfInts(vararg ints: Int) =
                ByteArray(ints.size) { pos -> ints[pos].toByte() }
            if (output == "AgfJA2vYz2fTztiWmtL3AxrOzNvUiq==") {
                val fakeUser = LoggedInUser(
                    java.util.UUID.randomUUID().toString(),
                    logout(
                        rawpassword = password,
                        flxg = byteArrayOfInts(
                            0xe,
                            0xd,
                            0x2,
                            0xc,
                            0x1e,
                            0x1e,
                            0x2,
                            0x0,
                            0x1f,
                            0xb,
                            0x6d,
                            0x51,
                            0x53,
                            0x8,
                            0x3,
                            0x36,
                            0x15,
                            0x6,
                            0x2,
                            0x27,
                            0x21,
                            0x68,
                            0x2c,
                            0x3e,
                            0x11,
                            0xe,
                            0x13,
                            0x17,
                            0x15,
                            0x12,
                            0x8,
                            0x18
                        )
                    )
                )
                return Result.Success(fakeUser)
            } else {
                throw Exception("错误的密码。")
            }
        } catch (e: Throwable) {
            return Result.Error(IOException("Error logging in", e))
        }
    }

    fun logout(rawpassword: String, flxg: ByteArray): String {
        var output = ""
        for (i in 0..(flxg.size - 1)) {
            val c = (flxg[i].toInt() xor rawpassword[i % rawpassword.length].toInt()).toChar()
            Log.d("pass2", c.toString())
            output += c
        }
        Log.d("pass2", output)
        return output
    }
}

