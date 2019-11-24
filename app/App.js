import React from 'react';
import { StyleSheet, Text, View, Dimensions, TouchableOpacity } from 'react-native';
import { DeviceMotion, Magnetometer } from 'expo-sensors';
import MapView, { Marker, Overlay, Polyline } from 'react-native-maps';
import * as Location from 'expo-location';
import * as Permissions from 'expo-permissions';
import Api from './api';

const SEND_INTERVAL = 30000;

function time() { 
  return (new Date()).getTime(); 
}

export default class Test extends React.Component {
  state = {
    initialized: false,
    errorMessage: null,
    measurementStart: 0,
    magnet: null,
    locations: [],
    sensors: [],
    reports: [],
    polyline: [],
    locationResult: null,
    coords: { latitude: 52.2297, longitude: -21.0122},
  }

  componentDidMount = async () => {
    let { status } = await Permissions.askAsync(Permissions.LOCATION);
    if (status !== 'granted') {
      this.setState({
        errorMessage: 'Permission to access location was denied',
      });
      return;
    }

    DeviceMotion.addListener(this.sensorsCallback);
    DeviceMotion.setUpdateInterval(10); // 100 updates/s
    Magnetometer.addListener(this.magnetometerCallback);
    Magnetometer.setUpdateInterval(10); // 100 updates/s

    Location.watchPositionAsync({timeInterval: 100}, this.locationCallback);
    this.state.measurementStart = time();

    setInterval(this.sendData, SEND_INTERVAL);

    this.setState({
      initialized: true
    });
  }

  locationCallback = (data) => {
    /*
      "coords": Object {
        "accuracy": 65,
        "altitude": 111.0348892211914,
        "altitudeAccuracy": 10,
        "heading": -1,
        "latitude": 52.22031458621937,
        "longitude": 20.98367600988036,
        "speed": -1,
      },
      "timestamp": 1574580128981.505,
    */
    this.state.locations.push({
      accuracy: data.coords.accuracy,
      altitude: data.coords.altitude,
      altitudeAccuracy: data.coords.altitudeAccuracy,
      heading: data.coords.heading,
      latitude: data.coords.latitude,
      longitude: data.coords.longitude,
      speed: data.coords.speed,
      time: data.timestamp,
    });

    if(this.state.polyline.length == 0
      || this.state.polyline[this.state.polyline.length - 1].latitude != data.coords.latitude
      || this.state.polyline[this.state.polyline.length - 1].longitude != data.coords.longitude) {

      this.state.polyline.push({
        latitude: data.coords.latitude, 
        longitude: data.coords.longitude
      });
      if(this.state.polyline.length > 300) {
        this.state.polyline.shift();
      }
    }

    this.setState({
      coords: { latitude: data.coords.latitude, longitude: data.coords.longitude}
    });
  }

  sensorsCallback = (data) => {
    if(!this.state.magnet) { // wait for magnetometer
      return;
    }
    this.state.sensors.push({
      acc: [data.acceleration.x.toFixed(3), data.acceleration.y.toFixed(3), data.acceleration.z.toFixed(3)],
      accg: [data.accelerationIncludingGravity.x.toFixed(3), data.accelerationIncludingGravity.y.toFixed(3), data.accelerationIncludingGravity.z.toFixed(3)],
      rotation: [data.rotation.alpha.toFixed(2), data.rotation.beta.toFixed(2), data.rotation.gamma.toFixed(2)],
      rotationrate: [data.rotationRate.alpha.toFixed(2), data.rotationRate.beta.toFixed(2), data.rotationRate.gamma.toFixed(2)],      
      magnet: this.state.magnet
    });
  }

  magnetometerCallback = (data) => {
    this.state.magnet = [data.x.toFixed(3), data.y.toFixed(3), data.z.toFixed(3)];
  }

  report = (type) => {
    this.state.reports.push({
      type: type,
      time: time()
    });
  }

  sendData = () => {
    Api.send({
      measurementStart: this.state.measurementStart,
      measurementEnd: time(),
      sensors: this.state.sensors,
      locations: this.state.locations,
      reports: this.state.reports
    });

    this.state.measurementStart = time();
    this.state.locations = [];
    this.state.sensors = [];
    this.state.reports = [];
  }

  render = () => {
    if(!this.state.initialized) {
      return (
        <View style={styles.container}>
          <Text>Intializing application</Text>
        </View>
      );  
    }
    if(this.state.errorMessage) {
      return (
        <View style={styles.container}>
          <Text>{this.state.errorMessage}</Text>
        </View>
      );  
    }
    return (
      <View style={styles.container}>
        <MapView 
          region={{ latitude: this.state.coords.latitude, longitude: this.state.coords.longitude,
             latitudeDelta: 0.0200, longitudeDelta: 0.0100 }}        
          style={styles.mapStyle}>
          <Marker
            coordinate={this.state.coords}
            title="Current position"
          />
        <Polyline
          coordinates={[...this.state.polyline]}
          strokeColor="#000" // fallback for when `strokeColors` is not supported by the map-provider
          strokeColors={[
            '#7F0000',
            '#00000000', // no color, creates a "long" gradient between the previous and next coordinate
            '#B24112',
            '#E5845C',
            '#238C23',
            '#7F0000'
          ]}
          strokeWidth={2}
        />          
        </MapView>
        <TouchableOpacity
            onPress={() => this.report(1)}
            style={[styles.bubble, styles.button]}
          >
            <Text style={styles.buttonText}>Zgłoś problem</Text>
          </TouchableOpacity>
        </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'flex-end',
    alignItems: 'center',
  },
  mapStyle: {
    ...StyleSheet.absoluteFillObject,
  },
  button: {
    width: 160,
    paddingHorizontal: 12,
    alignItems: 'center',
    marginHorizontal: 10,    
  },
  buttonContainer: {
    flexDirection: 'row',
    marginVertical: 20,
    backgroundColor: 'transparent',
  },
  bubble: {
    backgroundColor: 'rgba(255,50,50,0.2)',
    paddingHorizontal: 18,
    paddingVertical: 12,
    borderRadius: 20,
    marginBottom: 10
  },
});