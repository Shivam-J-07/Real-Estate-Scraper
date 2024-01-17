import axios from "axios";

export const fetchLatandLon = async (address: string) => {
  const api_key = process.env.NEXT_PUBLIC_MAPS_API_KEY;

  if (api_key) {
    try {
      const res = await axios.get(
        `https://maps.googleapis.com/maps/api/geocode/json?address=${address}&key=${api_key}`
      );
      const result = res.data.results[0].geometry.location;

      return { lat: result.lat, lon: result.lng };
    } catch (error) {
      console.error("An error occurred fetching lat and lon", error);
      return { lat: null, lon: null };
    }
  }

  return { lat: null, lon: null };
};
