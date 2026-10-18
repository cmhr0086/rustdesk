//! Server settings baked into this build. Leave `RENDEZVOUS_SERVER` empty to
//! behave like the official client.
//!
//! Values go into `OVERWRITE_SETTINGS`, so they win over the user's config
//! and `Config::set_option` refuses to store anything else for these keys.

use base::config::keys;
use hbb_common::config;

/// hbbs, `host[:port]`
const RENDEZVOUS_SERVER: &str = "";
/// Content of hbbs `id_ed25519.pub`
const RS_PUB_KEY: &str = "F9ZWfKQo668K+NF2fYbVZXs3hbc2plJbLWF8DOjYxqc=";
/// hbbr, `host[:port]`; empty means whatever hbbs hands out
const RELAY_SERVER: &str = "";
/// `http(s)://host[:port]`, only needed for an API server
const API_SERVER: &str = "";

pub fn apply() {
    if RENDEZVOUS_SERVER.is_empty() {
        return;
    }
    let mut settings = config::OVERWRITE_SETTINGS.write().unwrap();
    for (k, v) in [
        (keys::OPTION_CUSTOM_RENDEZVOUS_SERVER, RENDEZVOUS_SERVER),
        (keys::OPTION_KEY, RS_PUB_KEY),
        (keys::OPTION_RELAY_SERVER, RELAY_SERVER),
        (keys::OPTION_API_SERVER, API_SERVER),
    ] {
        if !v.is_empty() {
            settings.insert(k.to_owned(), v.to_owned());
        }
    }
    drop(settings);
    config::BUILTIN_SETTINGS
        .write()
        .unwrap()
        .insert(keys::OPTION_HIDE_SERVER_SETTINGS.to_owned(), "Y".to_owned());
}
