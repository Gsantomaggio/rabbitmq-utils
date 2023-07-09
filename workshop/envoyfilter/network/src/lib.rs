use std::collections::HashMap;

use byteorder::ByteOrder;
// use log::error;
use log::{error, info};
use proxy_wasm::traits::*;
use proxy_wasm::types::*;

/// A std Result with a lapin::Error error type
// pub type Result<T> = std::result::Result<T, Error>;
#[no_mangle]
pub fn _start() {
    proxy_wasm::set_log_level(LogLevel::Info);

    proxy_wasm::set_stream_context(|context_id, root_context_id| -> Box<dyn StreamContext> {
        Box::new(StreamingAuthorizer {
            context_id,
            root_context_id,
        })
    });

    proxy_wasm::set_root_context(|_root_context_id| -> Box<dyn RootContext> {
        Box::new(StreamingAuthorizer::new())
    });
}


struct StreamingAuthorizer {
    context_id: u32,
    root_context_id: u32,
}


impl Context for StreamingAuthorizer {}

impl StreamingAuthorizer {
    fn new() -> Self {
        return Self {
            context_id: 0,
            root_context_id: 0,
        };
    }

    fn parse(tou8: &&[u8]) {
        let length = byteorder::BigEndian::read_i32(&tou8);
        let command = byteorder::BigEndian::read_u16(&tou8[4..]);
        let version = byteorder::BigEndian::read_u16(&tou8[6..]);
        let mut index: i32 = 16;
        if command == 17 {
            let corr_id = byteorder::BigEndian::read_u32(&tou8[8..]);
            let _items = byteorder::BigEndian::read_u32(&tou8[12..]);

            let mut i = 0;
            info!("\x1b[0;32mHeader: protocol-length {:?} command {:?} version {:?}\x1b[0m",
                    length,
                    command,
                    version);
            while i < 6 {
                let len = byteorder::BigEndian::read_u16(&tou8[index as usize..]);
                index = index + 2 as i32;
                let end = index as usize + len as usize;
                let bytes = &tou8[index as usize..end as usize];
                let key = String::from_utf8(bytes.to_vec());
                index = index + len as i32;

                let len_v = byteorder::BigEndian::read_u16(&tou8[index as usize..]);
                index = index + 2 as i32;
                let end = index as usize + len_v as usize;
                let bytes_v = &tou8[index as usize..end as usize];
                let value = String::from_utf8(bytes_v.to_vec());
                index = index + len_v as i32;
                // mymap.insert(key.unwrap(), value.unwrap());
                info!("\x1b[0;33m Client Prop: {:?} - :{:?}\x1b[0m",
                key.unwrap(), value.unwrap());
                i = i + 1;
            }
        }
        if command == 2 {
            index = index + 1 as i32;
            let len = byteorder::BigEndian::read_u32(&tou8[index as usize..]);
            info!("\x1b[0;33m publihed  {:?} messages\x1b[0m",len);
        }
    }
}

impl RootContext for StreamingAuthorizer {
    fn on_vm_start(&mut self, _vm_configuration_size: usize) -> bool {
        info!("[RABBITMQ-WASM-FILTER] Init Streaming");
        true
    }

    fn on_tick(&mut self) {
        info!("[RABBITMQ-WASM-FILTER] ON TICK");
    }

    fn on_queue_ready(&mut self, queue_id: u32) {
        info!("[RABBITMQ-WASM-FILTER] ON QUEUE READY {}", queue_id);
    }
}

impl StreamContext for StreamingAuthorizer {
    fn on_new_connection(&mut self) -> Action {
        Action::Continue
    }


    fn on_downstream_data(&mut self, data_size: usize, end_of_stream: bool) -> Action {
        if let Some(data) = self.get_downstream_data(0, data_size) {
            let tou8: &[u8] = &data;
            // info!("Stream traffic-raw {:?}", tou8);
            Self::parse(&tou8);
            let version = byteorder::BigEndian::read_u16(&tou8[6..]);
            if version ==1 {
                error!("\x1b[0;31m Drop connection: VERSION {:?} not allowed \x1b[0m",
                version);
             return Action::Pause;
            }
       
        }
        return Action::Continue;
    }


    fn on_downstream_close(&mut self, _peer_type: PeerType) {
        // info!("[RABBITMQ-WASM-FILTER] DOWN CLOSE STREAM, Peer Type: {:?}", peer_type);
    }


    fn on_upstream_data(&mut self, _data_size: usize, _end_of_stream: bool) -> Action {
        return Action::Continue;

        //   if let Some(data) = self.get_upstream_data(0, _data_size) {
        // let tou8: &[u8] = &data;
        // let length = byteorder::BigEndian::read_u32(&tou8);
        // let command = byteorder::BigEndian::read_u16(&tou8[4..]);
        // let version = byteorder::BigEndian::read_u16(&tou8[6..]);
        // info!("\x1b[0;33m[RABBITMQ-WASM-FILTER] Header: protocol length {:?} command {:?} version {:?}\x1b[0m",
        //     length,
        //     command,
        //     version);
        // if command == 21 {
        //     info!("\x1b[0;31m[RABBITMQ-WASM-FILTER] Header: version ERROR {:?}\x1b[0m",
        //     version);
        //     return Action::Pause
        // }
        //     }
        // return Action::Continue
    }


    fn on_upstream_close(&mut self, _peer_type: PeerType) {
        // info!("[RABBITMQ-WASM-FILTER] CLOSE UP STREAM, Peer Type: {:?}", peer_type);
    }
}
