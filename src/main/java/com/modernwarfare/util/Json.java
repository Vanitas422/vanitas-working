package com.modernwarfare.util;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class Json {
    private Json() {}

    public static Object parseResource(String path) throws IOException {
        try (InputStream stream = Json.class.getResourceAsStream(path)) {
            if (stream == null) {
                throw new IOException("Missing resource: " + path);
            }
            return parse(new String(stream.readAllBytes(), StandardCharsets.UTF_8));
        }
    }

    public static Object parse(String input) {
        return new Parser(input).parse();
    }

    public static Map<String, Object> asObject(Object value) {
        if (value instanceof Map<?, ?> map) {
            Map<String, Object> result = new LinkedHashMap<>();
            for (Map.Entry<?, ?> entry : map.entrySet()) {
                result.put(String.valueOf(entry.getKey()), entry.getValue());
            }
            return result;
        }
        throw new IllegalArgumentException("Expected JSON object");
    }

    public static List<Object> asArray(Object value) {
        if (value instanceof List<?> list) {
            return new ArrayList<>(list);
        }
        throw new IllegalArgumentException("Expected JSON array");
    }

    public static String string(Map<String, Object> map, String key) { return String.valueOf(map.get(key)); }
    public static double number(Map<String, Object> map, String key) { return ((Number) map.get(key)).doubleValue(); }
    public static int integer(Map<String, Object> map, String key) { return ((Number) map.get(key)).intValue(); }
    public static boolean bool(Map<String, Object> map, String key) { return Boolean.TRUE.equals(map.get(key)); }

    private static final class Parser {
        private final String input;
        private int cursor;

        private Parser(String input) { this.input = input; }

        Object parse() {
            Object value = value();
            whitespace();
            if (cursor != input.length()) {
                throw new IllegalArgumentException("Trailing JSON at " + cursor);
            }
            return value;
        }

        private Object value() {
            whitespace();
            if (cursor >= input.length()) throw new IllegalArgumentException("Unexpected end of JSON");
            char c = input.charAt(cursor);
            return switch (c) {
                case '{' -> object();
                case '[' -> array();
                case '"' -> string();
                case 't' -> literal("true", Boolean.TRUE);
                case 'f' -> literal("false", Boolean.FALSE);
                case 'n' -> literal("null", null);
                default -> number();
            };
        }

        private Map<String, Object> object() {
            expect('{');
            Map<String, Object> map = new LinkedHashMap<>();
            whitespace();
            if (peek('}')) { cursor++; return map; }
            while (true) {
                String key = string();
                whitespace();
                expect(':');
                map.put(key, value());
                whitespace();
                if (peek('}')) { cursor++; return map; }
                expect(',');
            }
        }

        private List<Object> array() {
            expect('[');
            List<Object> list = new ArrayList<>();
            whitespace();
            if (peek(']')) { cursor++; return list; }
            while (true) {
                list.add(value());
                whitespace();
                if (peek(']')) { cursor++; return list; }
                expect(',');
            }
        }

        private String string() {
            expect('"');
            StringBuilder builder = new StringBuilder();
            while (cursor < input.length()) {
                char c = input.charAt(cursor++);
                if (c == '"') return builder.toString();
                if (c == '\\') {
                    char escaped = input.charAt(cursor++);
                    builder.append(switch (escaped) {
                        case '"' -> '"';
                        case '\\' -> '\\';
                        case '/' -> '/';
                        case 'b' -> '\b';
                        case 'f' -> '\f';
                        case 'n' -> '\n';
                        case 'r' -> '\r';
                        case 't' -> '\t';
                        default -> escaped;
                    });
                } else {
                    builder.append(c);
                }
            }
            throw new IllegalArgumentException("Unterminated string");
        }

        private Object number() {
            int start = cursor;
            while (cursor < input.length() && "-+.0123456789eE".indexOf(input.charAt(cursor)) >= 0) cursor++;
            String token = input.substring(start, cursor);
            if (token.contains(".") || token.contains("e") || token.contains("E")) return Double.parseDouble(token);
            return Long.parseLong(token);
        }

        private Object literal(String token, Object value) {
            if (!input.startsWith(token, cursor)) throw new IllegalArgumentException("Expected " + token);
            cursor += token.length();
            return value;
        }

        private void whitespace() {
            while (cursor < input.length() && Character.isWhitespace(input.charAt(cursor))) cursor++;
        }

        private boolean peek(char c) { return cursor < input.length() && input.charAt(cursor) == c; }
        private void expect(char c) {
            whitespace();
            if (!peek(c)) throw new IllegalArgumentException("Expected '" + c + "' at " + cursor);
            cursor++;
        }
    }
}
