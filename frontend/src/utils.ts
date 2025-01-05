import axios from "axios";

export const fetchLatandLon = async (address: string) => {
  const formattedAddress = encodeURIComponent(address).replace(/%20+/g, "+");
  try {
    const res = await axios.get(
      `https://nominatim.openstreetmap.org/search?q=${formattedAddress}&format=geojson`
    );
    const result = res.data.features[0];

    if (!result) {
      console.warn("Could not find lat and lon for address", address);
      return { lat: null, lon: null };
    }

    const [lon, lat] = result.geometry.coordinates;
    return { lat, lon };
  } catch (error) {
    console.error("An error occurred fetching lat and lon", error);
    return { lat: null, lon: null };
  }
};
