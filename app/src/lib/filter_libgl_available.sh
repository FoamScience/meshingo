filter_libgl_available() {
    if command -v ldconfig >/dev/null 2>&1; then
        if ldconfig -p 2>/dev/null | grep -q 'libGL.so.1'; then
            return 0
        fi
    fi
    if find /usr/lib /usr/local/lib /lib -name 'libGL.so.1*' 2>/dev/null | grep -q .; then
        return 0
    fi
    echo "❌ Error: libGL.so.1 not found. Please install OpenGL runtime (e.g. libgl1, mesa-libGL, or mesa-gl)."
    return 1
}
